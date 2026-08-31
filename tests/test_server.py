from pathlib import Path

from starlette.testclient import TestClient

from merkury.server import _get_app
from merkury.utils import get_python_files


def test_server(tmp_path):
    template_data = {
        "output_format": "html",
        "show_input_blocks": True,
        "toc": False,
        "author": "pytest",
    }
    path = Path("tests/dir")
    sub_paths = tuple(p.absolute() for p in get_python_files(path))
    out_path = Path(tmp_path, "out_dir")
    out_path.mkdir()
    expected_file = Path(out_path, "s1.html")
    assert not expected_file.exists()
    app = _get_app(sub_paths, out_path, template_data)
    with TestClient(app=app, follow_redirects=False) as client:
        assert client.get("/").status_code == 404
        assert client.get("/read/s1").status_code == 404
        assert client.get("/execute/s1").status_code == 303
        assert expected_file.is_file()
        assert client.get("/read/s1").status_code == 200
