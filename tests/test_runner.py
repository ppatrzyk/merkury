from merkury.runner_py import *
import pathlib

PY_SCRIPT = pathlib.Path("tests/script.py")

def test_prune_lines():
    assert prune_lines(["content", "", "content"]) == ["content", "", "content"]
    assert prune_lines(["content", "", ""]) == ["content"]
    assert prune_lines([]) == []

def test_execute_python():
    expected_code = [
        (["a = 1 + 2"], ""),
        (["""s = \"some string\""""], ""),
        (["""print(f"Test {s}")""", "#TITLE First section"], "Test some string\n"),
        (["b = a + 5"], ""),
        (["for _ in range(2):", """    print("loop test")""", "#TITLE Second section"], "loop test\nloop test\n")
    ]
    assert list(execute_python(PY_SCRIPT)) == expected_code
