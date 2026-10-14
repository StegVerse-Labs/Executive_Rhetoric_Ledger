#!/usr/bin/env python3
"""Standard-library runner for function-style tests (replaces pytest).

Usage: python tests/stdlib_testing.py tests/test_a.py [tests/test_b.py ...]

Collects module-level ``test_*`` functions in file order, supplies a fresh
``tmp_path`` directory to any test that declares that parameter, and exits
non-zero if any test fails. ``raises`` mirrors ``pytest.raises(exc, match=...)``.
"""
from __future__ import annotations

import contextlib
import importlib.util
import inspect
import re
import sys
import tempfile
import traceback
from pathlib import Path


@contextlib.contextmanager
def raises(expected: type[BaseException], match: str | None = None):
    try:
        yield
    except expected as exc:
        if match is not None and not re.search(match, str(exc)):
            raise AssertionError(f"{expected.__name__} raised but {match!r} not found in {str(exc)!r}") from exc
        return
    raise AssertionError(f"{expected.__name__} was not raised")


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    return module


def run(paths: list[str]) -> int:
    here = Path(__file__).resolve().parent
    # cwd (as `python -m pytest` did), tests/, and scripts/ for modules loaded by file path
    sys.path[:0] = [str(Path.cwd()), str(here), str(here.parent / "scripts")]
    passed, failed = 0, []
    for raw in paths:
        module = _load(Path(raw).resolve())
        tests = [(n, f) for n, f in vars(module).items() if n.startswith("test_") and inspect.isfunction(f) and f.__module__ == module.__name__]
        for name, func in tests:
            kwargs = {}
            with tempfile.TemporaryDirectory() as tmp:
                if "tmp_path" in inspect.signature(func).parameters:
                    kwargs["tmp_path"] = Path(tmp)
                try:
                    func(**kwargs)
                    passed += 1
                except Exception:
                    failed.append(f"{raw}::{name}")
                    traceback.print_exc()
    for item in failed:
        print(f"FAILED {item}")
    print(f"{passed} passed, {len(failed)} failed")
    return 1 if failed or passed == 0 else 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
