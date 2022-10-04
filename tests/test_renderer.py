from merkury.renderer import *
import pathlib
import re

def test_get_default_path():
    assert isinstance(get_default_path(pathlib.Path("abs/path/file.py"), "html"), pathlib.Path)
    assert re.search(r"^/abs/path/file_.*\.html$", str(get_default_path(pathlib.Path("/abs/path/file.py"), "html")))
    assert re.search(r"^rel/file_.*\.pdf$", str(get_default_path(pathlib.Path("rel/file.py"), "pdf")))

def test_join_chunks():
    assert list(join_chunks(zip([], []))) == []
    code = zip(
        (["""print("aaa")"""], ["a = 5", "b = 6"], ["""print("a")""", ""], ),
        ("aaa\n", "", "a\n", )
    )
    joined = [
        {"in": """print("aaa")\n""", "out": "aaa\n", "html": False, "markdown": False},
        {"in": """a = 5\nb = 6\nprint("a")\n\n""", "out": "a\n", "html": False, "markdown": False}
    ]
    assert list(join_chunks(code)) == joined
