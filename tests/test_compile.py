"""
Import-smoke-test every candidate's main.py

We create a *stub* AlgorithmImports module on-the-fly so Lean classes
like QCAlgorithm, Resolution, MovingAverageType resolve during import.
"""

import importlib.util, pathlib, sys, types, pytest

# ------------------------------------------------------------------
#  Create a minimal stub for AlgorithmImports that satisfies `import *`
# ------------------------------------------------------------------
stub = types.ModuleType("AlgorithmImports")

class QCAlgorithm:  # empty shell just so hasattr checks pass
    pass

class Resolution:
    Minute = 0
    Daily = 1

class MovingAverageType:
    Wilders = 0

# Expose names expected in user code
stub.QCAlgorithm = QCAlgorithm
stub.Resolution = Resolution
stub.MovingAverageType = MovingAverageType

# Register the stub so `import AlgorithmImports` works
sys.modules["AlgorithmImports"] = stub
# ------------------------------------------------------------------

C_ROOT = pathlib.Path("factory/candidates")

def main_files():
    """Yield every main.py under factory/candidates/ALG_*/"""
    return C_ROOT.glob("ALG_*/main.py")

@pytest.mark.timeout(2)
@pytest.mark.parametrize("main_py", main_files())
def test_import(main_py):
    spec = importlib.util.spec_from_file_location(main_py.stem, main_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
