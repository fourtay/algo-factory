import importlib.util, pathlib, pytest

C_ROOT = pathlib.Path("factory/candidates")

def main_files():
    return C_ROOT.glob("ALG_*/main.py")

@pytest.mark.timeout(2)
@pytest.mark.parametrize("main_py", main_files())
def test_import(main_py):
    spec = importlib.util.spec_from_file_location(main_py.stem, main_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
