from merkury.runner import *
import pathlib

def test_execute():
    script = pathlib.Path("tests/script.py")
    expected_code = [
        (["a = 1 + 2"], ""),
        (["""s = \"some string\"""", ""], ""),
        (["""print(f"Test {s}")""", ""], "Test some string\n"),
        (["b = a + 5", ""], "")
    ]
    code, _duration = execute(script)
    assert list(code) == expected_code
