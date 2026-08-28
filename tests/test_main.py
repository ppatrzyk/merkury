from merkury.main import main

import pytest

def test_main():
    bad_args = (
        ["bad"],
        ["-o", "/dev/null", "-f", "badformat", "tests/script.py"],
        ["-o", "/dev/null", "-f", "md", "tests/dir"],
    )
    for arg_list in bad_args:
        with pytest.raises(Exception) as exc_info:
            main(arg_list)

def test_main():
    assert main(["-o", "/dev/null", "-f", "md", "tests/badscript.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "md", "tests/script.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "html", "tests/script.py"]) == 0
