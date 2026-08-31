from merkury.main import main

from pathlib import Path
import pytest

def test_main_errors(tmp_path):
    bad_args = (
        ["bad"],
        ["-o", "/dev/null", "-f", "md", "-p", "NA", "tests/script.py"],
        ["-o", "/dev/null", "-f", "badformat", "tests/script.py"],
        ["-o", "/dev/null", "-f", "md", "tests/dir/bad"],
        ["-o", "/dev/null", "-f", "md", "/dev/null"],
        ["-o", "/dev/null", "-f", "md", "bad"],
        ["-o", "/dev/null", "-f", "md", "bad.py"],
        ["-o", "/dev/null", "-f", "md", "batch", "tests/script.py"],
        ["-o", Path(tmp_path, "file.html"), "-f", "md", "batch", "tests/dir"],
    )
    for arg_list in bad_args:
        with pytest.raises(Exception) as exc_info:
            logging.debug(arg_list)
            main(arg_list)

def test_main():
    assert main(["-o", "/dev/null", "-f", "md", "tests/badscript.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "md", "tests/script.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "html", "tests/script.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "html", "batch", "tests/dir"]) == 0
