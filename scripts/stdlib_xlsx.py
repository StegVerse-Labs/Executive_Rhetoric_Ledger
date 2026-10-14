"""Minimal standard-library .xlsx access (replaces openpyxl).

Covers the surface these scripts use:
- read: load_workbook(file) -> Workbook with .sheetnames, .worksheets, wb[name];
  Worksheet .title, .max_row, .max_column, .cell(row, col).value,
  .iter_rows(min_row, max_row, values_only=True). Cached cell values are
  returned (the data_only behaviour): shared/inline strings as str, booleans as
  bool, numbers as int or float, and date-formatted numbers as datetime.
  max_row/max_column honour the sheet's declared <dimension>.
- write (fixtures only): Workbook(), .active, .create_sheet(title),
  ws["A1"] = value, .save(file).
"""
from __future__ import annotations

import re
import zipfile
from datetime import datetime, timedelta
from typing import Any, BinaryIO, Iterator
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
_REF = re.compile(r"^([A-Z]+)(\d+)$")


def column_index_from_string(letters: str) -> int:
    index = 0
    for char in letters.upper():
        if not "A" <= char <= "Z":
            raise ValueError(f"invalid column letters: {letters!r}")
        index = index * 26 + (ord(char) - 64)
    return index


def get_column_letter(index: int) -> str:
    letters = ""
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(65 + rem) + letters
    return letters


def _split_ref(ref: str) -> tuple[int, int]:
    match = _REF.match(ref)
    if not match:
        raise ValueError(f"invalid cell reference: {ref!r}")
    return int(match.group(2)), column_index_from_string(match.group(1))


class Cell:
    __slots__ = ("value",)

    def __init__(self, value: Any = None):
        self.value = value


class Worksheet:
    def __init__(self, title: str):
        self.title = title
        self._cells: dict[tuple[int, int], Any] = {}
        self._declared = (0, 0)

    @property
    def max_row(self) -> int:
        return max(max((r for r, _ in self._cells), default=1), self._declared[0])

    @property
    def max_column(self) -> int:
        return max(max((c for _, c in self._cells), default=1), self._declared[1])

    def cell(self, row: int, column: int) -> Cell:
        return Cell(self._cells.get((row, column)))

    def __getitem__(self, ref: str) -> Cell:
        return self.cell(*_split_ref(ref))

    def __setitem__(self, ref: str, value: Any) -> None:
        self._cells[_split_ref(ref)] = value

    def iter_rows(self, min_row: int = 1, max_row: int | None = None, values_only: bool = False) -> Iterator[tuple]:
        last_col = self.max_column
        for row in range(min_row, (max_row or self.max_row) + 1):
            values = tuple(self._cells.get((row, col)) for col in range(1, last_col + 1))
            yield values if values_only else tuple(Cell(v) for v in values)


class Workbook:
    def __init__(self):
        self.worksheets: list[Worksheet] = [Worksheet("Sheet")]
        self._sheet_order: list[str] | None = None  # includes chart sheets when loaded

    @property
    def active(self) -> Worksheet:
        return self.worksheets[0]

    @property
    def sheetnames(self) -> list[str]:
        if self._sheet_order is not None:
            return list(self._sheet_order)
        return [ws.title for ws in self.worksheets]

    def __getitem__(self, name: str) -> Worksheet:
        for ws in self.worksheets:
            if ws.title == name:
                return ws
        raise KeyError(f"Worksheet {name} does not exist.")

    def create_sheet(self, title: str) -> Worksheet:
        ws = Worksheet(title)
        self.worksheets.append(ws)
        return ws

    def save(self, target: str | BinaryIO) -> None:
        sheets = self.worksheets
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("[Content_Types].xml",
                '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                '<Default Extension="xml" ContentType="application/xml"/>'
                '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sheets) + 1))
                + "</Types>")
            zf.writestr("_rels/.rels",
                f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="{PKG_REL_NS}">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
            zf.writestr("xl/workbook.xml",
                f'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="{NS["m"]}" xmlns:r="{REL_NS}"><sheets>'
                + "".join(f'<sheet name="{escape(ws.title, {chr(34): "&quot;"})}" sheetId="{i}" r:id="rId{i}"/>' for i, ws in enumerate(sheets, 1))
                + "</sheets></workbook>")
            zf.writestr("xl/_rels/workbook.xml.rels",
                f'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="{PKG_REL_NS}">'
                + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(sheets) + 1))
                + "</Relationships>")
            for i, ws in enumerate(sheets, 1):
                rows: dict[int, list[str]] = {}
                for (r, c), value in sorted(ws._cells.items()):
                    if value is None:
                        continue
                    ref = f"{get_column_letter(c)}{r}"
                    if isinstance(value, bool):
                        xml = f'<c r="{ref}" t="b"><v>{int(value)}</v></c>'
                    elif isinstance(value, (int, float)):
                        xml = f'<c r="{ref}"><v>{value!r}</v></c>'
                    else:
                        xml = f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'
                    rows.setdefault(r, []).append(xml)
                body = "".join(f'<row r="{r}">{"".join(cells)}</row>' for r, cells in sorted(rows.items()))
                zf.writestr(f"xl/worksheets/sheet{i}.xml",
                    f'<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="{NS["m"]}"><sheetData>{body}</sheetData></worksheet>')


def _number(text: str) -> int | float:
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    return float(text)


BUILTIN_DATE_FORMATS = set(range(14, 23)) | {45, 46, 47}
EXCEL_EPOCH = datetime(1899, 12, 30)


def _is_date_code(code: str) -> bool:
    stripped = re.sub(r'"[^"]*"|\\.|\[[^\]]*\]', "", code.split(";")[0])
    return bool(re.search(r"[dmyhs]", stripped, re.IGNORECASE)) and "General" not in stripped


def _date_styles(zf: zipfile.ZipFile, names: set[str]) -> set[int]:
    """Indexes of cellXfs entries whose number format is a date/time format."""
    if "xl/styles.xml" not in names:
        return set()
    root = ET.fromstring(zf.read("xl/styles.xml"))
    custom = {int(n.get("numFmtId")): n.get("formatCode", "") for n in root.iterfind("m:numFmts/m:numFmt", NS)}
    dates = set()
    for index, xf in enumerate(root.iterfind("m:cellXfs/m:xf", NS)):
        fmt = int(xf.get("numFmtId", "0"))
        if fmt in BUILTIN_DATE_FORMATS or (fmt in custom and _is_date_code(custom[fmt])):
            dates.add(index)
    return dates


def _text(node: ET.Element) -> str:
    return "".join(t.text or "" for t in node.iter(f"{{{NS['m']}}}t"))


def load_workbook(source: str | BinaryIO, read_only: bool = True, data_only: bool = True) -> Workbook:
    """Read cached cell values from an .xlsx file or file-like object."""
    with zipfile.ZipFile(source) as zf:
        names = set(zf.namelist())
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            shared = [_text(si) for si in root.findall("m:si", NS)]
        date_styles = _date_styles(zf, names)
        rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        targets = {rel.get("Id"): rel.get("Target") for rel in rels_root}
        kinds = {rel.get("Id"): rel.get("Type", "").rsplit("/", 1)[-1] for rel in rels_root}
        book = ET.fromstring(zf.read("xl/workbook.xml"))
        wb = Workbook()
        wb.worksheets = []
        wb._sheet_order = []
        for sheet in book.find("m:sheets", NS):
            rel_id = sheet.get(f"{{{REL_NS}}}id")
            wb._sheet_order.append(sheet.get("name"))
            if kinds.get(rel_id) != "worksheet":
                continue  # chart sheets are named but hold no cells, as in openpyxl
            ws = wb.create_sheet(sheet.get("name"))
            target = targets[rel_id].lstrip("/")
            path = target if target.startswith("xl/") else f"xl/{target}"
            root = ET.fromstring(zf.read(path))
            dimension = root.find("m:dimension", NS)
            if dimension is not None and dimension.get("ref"):
                last = dimension.get("ref").split(":")[-1].replace("$", "")
                if _REF.match(last):
                    ws._declared = _split_ref(last)
            for c in root.iter(f"{{{NS['m']}}}c"):
                kind, v = c.get("t"), c.find("m:v", NS)
                if kind == "inlineStr":
                    value: Any = _text(c.find("m:is", NS))
                elif v is None or v.text is None:
                    continue
                elif kind == "s":
                    value = shared[int(v.text)]
                elif kind == "b":
                    value = v.text == "1"
                elif kind in ("str", "e"):
                    value = v.text
                else:
                    value = _number(v.text)
                    if int(c.get("s", "0")) in date_styles:
                        value = EXCEL_EPOCH + timedelta(days=value)
                ws._cells[_split_ref(c.get("r"))] = value
        return wb
