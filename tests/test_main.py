import shutil
from pathlib import Path

import pytest

from merkury.main import main


def test_main_errors(tmp_path):
    with pytest.raises(Exception):  # noqa
        main(["bad"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "badformat", "tests/scripts/script.py"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "md", "tests/dir/bad"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "md", "/dev/null"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "md", "bad"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "md", "bad.py"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "md", "batch", "tests/scripts/script.py"])
    with pytest.raises(Exception):  # noqa
        out = Path(tmp_path, "file.html")
        out.touch()
        main(["-o", str(out), "-f", "md", "batch", "tests/dir"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "md", "batch", "tests/dirnotexisting"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "md", "-p", "NA", "batch", "tests/dir"])
    server_out_baddir = Path(tmp_path, "server_bad")
    server_out_baddir.touch()
    with pytest.raises(Exception):  # noqa
        main(["-o", str(server_out_baddir), "-f", "html", "server", "tests/dir"])
    with pytest.raises(Exception):  # noqa
        main(["-o", "/dev/null", "-f", "html", "server", "tests/dir"])
    server_out = Path(tmp_path, "server_ok")
    server_out.mkdir()
    with pytest.raises(Exception):  # noqa
        main(["-o", str(server_out), "-f", "md", "server", "tests/dir"])


def test_main(tmp_path):
    # single
    assert main(["-o", "/dev/null", "-f", "md", "tests/scripts/badscript.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "md", "tests/scripts/script.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "html", "tests/scripts/script.py"]) == 0
    script_path = Path(tmp_path, "nested/scripts/script.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(Path("tests/scripts/script.py"), script_path)
    assert main(["-f", "html", str(script_path)]) == 0
    assert Path(tmp_path, "nested/scripts/script.html").exists()
    out_file_path = Path(tmp_path, "nested/outputs/custom.html")
    assert main(["-o", str(out_file_path), "-f", "html", str(script_path)]) == 0
    assert out_file_path.exists()
    out_dir_path = Path(tmp_path, "nested/nested/customoutdir")
    assert main(["-o", str(out_dir_path), "-f", "html", str(script_path)]) == 0
    assert out_dir_path.exists()
    assert out_dir_path.is_dir()
    assert Path(out_dir_path, "script.html").is_file()
    assert main(["-o", "/dev/null", "-f", "html", "tests/scripts/script.py", "arg1"]) == 0
    # batch
    assert main(["-o", "/dev/null", "-f", "html", "batch", "tests/dir"]) == 0
    batch_dir_out = Path(tmp_path, "batch_dir_out")
    batch_dir_out.mkdir()
    assert not Path(batch_dir_out, "s1.html").exists()
    assert main(["-o", str(batch_dir_out), "-f", "html", "batch", "tests/dir"]) == 0
    assert Path(batch_dir_out, "s1.html").exists()
    batch_dir_in = Path(tmp_path, "batch_dir_in")
    shutil.copytree(Path("tests/dir"), batch_dir_in, dirs_exist_ok=True)
    assert not Path(batch_dir_in, "s1.html").exists()
    assert main(["-f", "html", "batch", str(batch_dir_in)]) == 0
    assert Path(batch_dir_in, "s1.html").exists()
    batch_empty_dir_in = Path(tmp_path, "batch_empty_dir_in")
    batch_empty_dir_in.mkdir()
    assert main(["-f", "html", "batch", str(batch_empty_dir_in)]) == 0
    assert main(["-o", "/dev/null", "-f", "html", "batch", "tests/dir", "arg1"]) == 0
    # server runs indefinitely, correct config tested in test_server.py

def test_main_args(tmp_path):
    script_path = Path("tests/scripts/args.py")
    for i, script_args in enumerate([[], ["arg1", "arg2"], ["456", "567"], ]):
        report_path = Path(tmp_path, f"args{i}.md")
        assert main(["-f", "md", "-o", str(report_path), str(script_path)] + script_args) == 0
        assert report_path.exists()
        with report_path.open("r") as file:
            report = file.read()
        result = "__NOT_PRINTED__"
        try:
            result = report.split("_Out_", 1)[1].split("__start__", 1)[1].split("__end__", 1)[0]
        except:
            pass
        assert str(script_path) in result
        for arg in script_args:
            assert arg in result
