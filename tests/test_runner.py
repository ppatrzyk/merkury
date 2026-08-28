from merkury.runner_py import execute_python, _prune_lines
import pathlib

PY_SCRIPT = pathlib.Path("tests/script.py")
PY_BAD_SCRIPT = pathlib.Path("tests/badscript.py")

def test_prune_lines():
    assert _prune_lines(["content", "", "content"]) == ["content", "", "content"]
    assert _prune_lines(["content", "", ""]) == ["content"]
    assert _prune_lines([]) == []

def test_execute_python():
    expected_code = [
        (["a = 1 + 2"], ""),
        (["""_long = \"h9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfE\""""], ""),
        (["""s = \"some string\""""], ""),
        (["""print(f"Test {s}")""", "#TITLE First section"], "Test some string\n"),
        (["b = a + 5"], ""),
        (["for _ in range(2):", """    print("loop test")""", "#TITLE Second section"], "loop test\nloop test\n")
    ]
    _duration, code = execute_python(PY_SCRIPT)
    assert list(code) == expected_code

def test_execute_bad_python():
    expected_code = [
        (["""print("first line")"""], "first line\n"),
        (["a = 1/-1"], ""),
        (["b = 1/0"], "ZeroDivisionError: division by zero\n"),
    ]
    _duration, code = execute_python(PY_BAD_SCRIPT)
    assert list(code) == expected_code
