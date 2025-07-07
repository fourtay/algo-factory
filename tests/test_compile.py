"""
tests/test_compile.py

• Walks every factory/candidates/ALG_*/main.py
• Stubs AlgorithmImports + Slice so strategies compile without Lean.
• Fails fast if import takes > 2 s or raises anything else.
"""

import importlib.util
import builtins
from pathlib import Path

import pytest

CANDIDATE_DIR = Path("factory/candidates")
MAIN_GLOBS = list(CANDIDATE_DIR.glob("ALG_*/main.py"))


def main_files():
    """Return list[Path] of main.py files to parametrize."""
    return MAIN_GLOBS


# --- Stubs so imports don’t blow up -------------------------------------------------
# A minimal AlgorithmImports that defines the symbols strategies usually expect.
# We only stub the names used by generated code (QCAlgorithm, Slice, Resolution,
# MovingAverageType).  Anything else will raise, which is fine for the gate.

class _QCAlgorithmStub:
    """Bare-minimum stand-in for QCAlgorithm."""
    def __getattr__(self, name):
        # allow any attr to return a lambda that swallows args and returns None
        return lambda *args, **kwargs: None


class _EnumStub:
    """Simple enum-like stub (e.g. Resolution.Daily)."""
    def __getattr__(self, name):
        return name


builtins.QCAlgorithm = _QCAlgorithmStub  # type: ignore
builtins.Slice = dict                      # minimal alias – behaves like a dict
builtins.Resolution = _EnumStub()          # Resolution.Daily etc.
builtins.MovingAverageType = _EnumStub()   # MovingAverageType.Wilders etc.

# ------------------------------------------------------------------------------------


@pytest.mark.timeout(2)
@pytest.mark.parametrize("main_py", main_files())
def test_import(main_py: Path):
    """Import each main.py and ensure it compiles with the stubs above."""
    spec = importlib.util.spec_from_file_location(main_py.stem, main_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # noqa: S301  (we’re intentionally importing)
