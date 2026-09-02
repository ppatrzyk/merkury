import pathlib

from merkury.runner_py import _execute_python, _prune_lines

PY_SCRIPT = pathlib.Path("tests/scripts/script.py")
PY_BAD_SCRIPT = pathlib.Path("tests/scripts/badscript.py")


def test_prune_lines():
    assert _prune_lines(["content", "", "content"]) == ["content", "", "content"]
    assert _prune_lines(["content", "", ""]) == ["content"]
    assert _prune_lines([]) == []


def test_execute_python():
    # durations stripped in expected_code (3rd tuple element)
    expected_code = [
        (["a = 1 + 2"], ""),
        (
            [
                """_long = \"h9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfEh9eIr8o0rZQ8cpfJ2LG31HfE\""""
            ],
            "",
        ),
        (["""s = \"some string\""""], ""),
        (["""print(f"Test {s}")""", "#TITLE First section"], "Test some string\n"),
        (["b = a + 5"], ""),
        (
            [
                "for _ in range(2):",
                """    print("loop test")""",
                "#TITLE Second section",
            ],
            "loop test\nloop test\n",
        ),
    ]
    _duration, code = _execute_python(PY_SCRIPT)
    assert [
        (code_in, code_out) for code_in, code_out, _duration in list(code)
    ] == expected_code


def test_execute_bad_python():
    # durations stripped in expected_code (3rd tuple element)
    expected_code = [
        (["""print("first line")"""], "first line\n"),
        (["a = 1/-1"], ""),
        (["b = 1/0"], "ZeroDivisionError: division by zero\n"),
    ]
    _duration, code = _execute_python(PY_BAD_SCRIPT)
    assert [
        (code_in, code_out) for code_in, code_out, _duration in list(code)
    ] == expected_code
