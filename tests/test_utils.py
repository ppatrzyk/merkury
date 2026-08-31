from merkury.utils import (
    _get_default_file_name,
    _get_default_path,
    process_output_path,
    get_report_path
)
from pathlib import Path
import re

def test_get_default_file_name():
    assert str(_get_default_file_name(Path("rel/file.py"), "html", False)) == "file.html"
    assert str(_get_default_file_name(Path("/abs/file.py"), "html", False)) == "file.html"
    assert re.search(r"^file_.*\.html$", str(_get_default_file_name(Path("rel/file.py"), "html", True)))
    assert re.search(r"^file_.*\.html$", str(_get_default_file_name(Path("/abs/file.py"), "html", True)))

def test_get_default_path():
    assert isinstance(_get_default_path(Path("abs/path/file.py"), "html", True), Path)
    assert re.search(r"^/abs/path/file_.*\.html$", str(_get_default_path(Path("/abs/path/file.py"), "html", True)))
    assert re.search(r"^rel/file_.*\.pdf$", str(_get_default_path(Path("rel/file.py"), "pdf", True)))
    assert re.search(r"^rel/filepy_.*\.html$", str(_get_default_path(Path("rel/filepy"), "html", True)))
    assert str(_get_default_path(Path("/abs/path/file.py"), "html", False)) == "/abs/path/file.html"
    assert str(_get_default_path(Path("rel/file.py"), "pdf", False)) == "rel/file.pdf"
    assert str(_get_default_path(Path("rel/filepy"), "html", False)) == "rel/filepy.html"

def test_process_output_path(tmp_path):
    assert process_output_path(None) is None
    existing_file_path = Path(tmp_path, "existing_file.html")
    existing_file_path.touch()
    assert process_output_path(existing_file_path) == existing_file_path
    existing_dir_path = Path(tmp_path, "existing_dir")
    existing_dir_path.mkdir()
    assert process_output_path(existing_dir_path) == existing_dir_path
    new_file_path = Path(tmp_path, "new_file.html")
    assert not new_file_path.exists()
    assert process_output_path(new_file_path) == new_file_path
    assert new_file_path.exists()
    assert new_file_path.is_file()
    new_dir_path = Path(tmp_path, "new_dir")
    assert not new_dir_path.exists()
    assert process_output_path(new_dir_path) == new_dir_path
    assert new_dir_path.exists()
    assert new_dir_path.is_dir()
    nested_file_path = Path(tmp_path, "customdir/customdir/script.html")
    assert not nested_file_path.exists()
    assert not nested_file_path.parent.exists()
    assert process_output_path(nested_file_path) == nested_file_path
    assert nested_file_path.is_file()
    nested_dir_path = Path(tmp_path, "customdir/customdir1")
    assert not nested_dir_path.exists()
    assert process_output_path(nested_dir_path) == nested_dir_path
    assert nested_dir_path.is_dir()

def test_get_report_path(tmp_path):
    script_path = Path(tmp_path, "script.py")
    script_path.touch()
    assert get_report_path(script_path, None, "html", False) == Path(tmp_path, "script.html")
    passed_path_file = Path(tmp_path, "customdir1/customdir1/custom.html")
    assert get_report_path(script_path, passed_path_file, "html", False) == passed_path_file
    passed_dir_file = Path(tmp_path, "customdir1/customdir2")
    passed_dir_file.mkdir(parents=True, exist_ok=True)
    assert get_report_path(script_path, passed_dir_file, "html", False) == Path(tmp_path, "customdir1/customdir2/script.html")
