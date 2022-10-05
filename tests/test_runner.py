from merkury.runner import *
import pathlib

def test_execute_python():
    script = pathlib.Path("tests/script.py")
    expected_code = [
        (["a = 1 + 2"], ""),
        (["""s = \"some string\"""", ""], ""),
        (["""print(f"Test {s}")""", ""], "Test some string\n"),
        (["b = a + 5", ""], "")
    ]
    code, _duration = execute_python(script)
    assert list(code) == expected_code

def test_execute_sqlite():
    # TODO
    assert False
