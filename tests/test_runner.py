from merkury.runner_py import *
import pathlib

PY_SCRIPT = pathlib.Path("tests/script.py")
PY_BAD_SCRIPT = pathlib.Path("tests/badscript.py")

def test_prune_lines():
    assert prune_lines(["content", "", "content"]) == ["content", "", "content"]
    assert prune_lines(["content", "", ""]) == ["content"]
    assert prune_lines([]) == []

def test_execute_python():
    expected_code = [
        (["a = 1 + 2"], ""),
        (["""_long = \"h9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfE\""""], ""),
        (["""s = \"some string\""""], ""),
        (["""print(f"Test {s}")""", "#TITLE First section"], "Test some string\n"),
        (["b = a + 5"], ""),
        (["for _ in range(2):", """    print("loop test")""", "#TITLE Second section"], "loop test\nloop test\n")
    ]
    assert list(execute_python(PY_SCRIPT)) == expected_code

def test_execute_bad_python():
    expected_code = [
        (["""print("first line")"""], "first line\n"),
        (["a = 1/-1"], ""),
        (["b = 1/0"], "ZeroDivisionError: division by zero\n"),
    ]
    assert list(execute_python(PY_BAD_SCRIPT)) == expected_code
