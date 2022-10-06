from merkury.runner_py import *
from merkury.runner_sql import *
import pathlib

PY_SCRIPT = pathlib.Path("tests/script.py")
SQL_SCRIPT = pathlib.Path("tests/script.sql")

def test_execute_python():
    expected_code = [
        (["a = 1 + 2"], ""),
        (["""s = \"some string\"""", ""], ""),
        (["""print(f"Test {s}")""", ""], "Test some string\n"),
        (["b = a + 5", ""], "")
    ]
    assert list(execute_python(PY_SCRIPT)) == expected_code

def test_generate_satements():
    expected = [
        ["""select "string1";"""],
        ["select", "", """  "string2";"""],
        ["create table", " test(id int);"],
        ["-- comment"]
    ]
    assert generate_satements(SQL_SCRIPT) == expected

def test_execute_sqlite():
    expected_code = [
        (["""select "string1";"""], "string1"),
        (["select", "", """  "string2";"""], "string2"),
        (["create table", " test(id int);"], ""),
        (["-- comment"], ""),
    ]
    assert list(execute_sqlite(":memory:", SQL_SCRIPT)) == expected_code
