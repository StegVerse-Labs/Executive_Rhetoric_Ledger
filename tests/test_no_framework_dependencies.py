"""Guard: workflows install nothing and Python code imports no framework packages."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {"jsonschema", "referencing", "pytest", "openpyxl", "requests", "bs4", "lxml", "pandas", "feedparser", "yaml"}


def test_workflows_install_no_packages():
    offenders = [p.name for p in (ROOT / ".github" / "workflows").glob("*.y*ml") if "pip install" in p.read_text(encoding="utf-8")]
    assert not offenders, offenders


def test_python_imports_only_standard_library():
    offenders = []
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) and node.module and node.level == 0 else []
            offenders += [f"{path.relative_to(ROOT)}:{n}" for n in names if n.split(".")[0] in FORBIDDEN]
    assert not offenders, offenders
