from merkury.utils import *
import pathlib
import re

def test_get_default_path():
    assert isinstance(get_default_path(pathlib.Path("abs/path/file.py"), "html"), pathlib.Path)
    assert re.search(r"^/abs/path/file_.*\.html$", str(get_default_path(pathlib.Path("/abs/path/file.py"), "html")))
    assert re.search(r"^rel/file_.*\.pdf$", str(get_default_path(pathlib.Path("rel/file.py"), "pdf")))
    assert re.search(r"^rel/filepy_.*\.html$", str(get_default_path(pathlib.Path("rel/filepy"), "html")))
