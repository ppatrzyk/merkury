from merkury.main import main

from pathlib import Path
import shutil
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
        ["-o", Path(tmp_path, "file.exe"), "-f", "md", "batch", "tests/dir"],
        ["-o", Path(tmp_path, "baddirectory"), "-f", "md", "batch", "tests/dir"],
        ["-o", "/dev/null", "-f", "md", "batch", "tests/dirnotexisting"],
    )
    for arg_list in bad_args:
        with pytest.raises(Exception) as exc_info:
            logging.debug(arg_list)
            main(arg_list)

def test_main(tmp_path):
    # single
    assert main(["-o", "/dev/null", "-f", "md", "tests/badscript.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "md", "tests/script.py"]) == 0
    assert main(["-o", "/dev/null", "-f", "html", "tests/script.py"]) == 0
    script_path = Path(tmp_path, "nested/scripts/script.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(Path("tests/script.py"), script_path)
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
