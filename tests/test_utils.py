from merkury.utils import *
import pathlib
import re

def test_get_default_path():
    assert isinstance(get_default_path(pathlib.Path("abs/path/file.py"), "html", True), pathlib.Path)
    assert re.search(r"^/abs/path/file_.*\.html$", str(get_default_path(pathlib.Path("/abs/path/file.py"), "html", True)))
    assert re.search(r"^rel/file_.*\.pdf$", str(get_default_path(pathlib.Path("rel/file.py"), "pdf", True)))
    assert re.search(r"^rel/filepy_.*\.html$", str(get_default_path(pathlib.Path("rel/filepy"), "html", True)))
    assert str(get_default_path(pathlib.Path("/abs/path/file.py"), "html", False)) == "/abs/path/file.html"
    assert str(get_default_path(pathlib.Path("rel/file.py"), "pdf", False)) == "rel/file.pdf"
    assert str(get_default_path(pathlib.Path("rel/filepy"), "html", False)) == "rel/filepy.html"
