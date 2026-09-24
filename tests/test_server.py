import re
from pathlib import Path

from starlette.testclient import TestClient

from merkury.server import _get_app
from merkury.utils import get_python_files

SERVER_TEMPLATE_DATA = {
    "output_format": "html",
    "show_input_blocks": False,
    "toc": False,
    "author": "pytest",
}


def test_server_execution(tmp_path):
    path = Path("tests/dir")
    sub_paths = tuple(p.absolute() for p in get_python_files(path))
    out_path = Path(tmp_path, "out_dir_execution")
    out_path.mkdir()
    expected_file = Path(out_path, "s1.html")
    assert not expected_file.exists()
    app = _get_app(sub_paths, out_path, SERVER_TEMPLATE_DATA)
    with TestClient(app=app, follow_redirects=False) as client:
        home = client.get("/")
        assert home.status_code == 200
        assert not re.search(
            r"href=\"\/execute\/bad",
            home.text,
        )
        assert re.search(
            r"href=\"\/execute\/s1\"",
            home.text,
        )
        assert re.search(
            r"href=\"\/read\/s1\"",
            home.text,
        )
        assert client.get("/read/s1").status_code == 404
        assert client.get("/execute/s1").status_code == 303
        assert expected_file.is_file()
        assert client.get("/read/s1").status_code == 200


def test_server_args(tmp_path):
    sub_paths = (Path("tests/scripts/args.py").absolute(),)
    out_path = Path(tmp_path, "out_dir_args")
    out_path.mkdir()
    app = _get_app(sub_paths, out_path, SERVER_TEMPLATE_DATA)
    with TestClient(app=app, follow_redirects=False) as client:
        arg1 = "arg123456"
        arg2 = "arg7890"
        assert (
            client.get(
                f"/execute/args?arg={arg1}&arg={arg2}&otherarg=otherarg"
            ).status_code
            == 303
        )
        report = client.get("/read/args").text
        result = "__NOT_PRINTED__"
        try:
            result = report.split("__start__", 1)[1].split("__end__", 1)[0]
        except:
            pass
        assert arg1 in result
        assert arg2 in result
        assert not "otherarg" in result


def test_server_stdin(tmp_path):
    sub_paths = (Path("tests/scripts/stdin.py").absolute(),)
    out_path = Path(tmp_path, "out_dir_stdin")
    out_path.mkdir()
    app = _get_app(sub_paths, out_path, SERVER_TEMPLATE_DATA)
    with TestClient(app=app, follow_redirects=False) as client:
        body = "body123456"
        assert client.post("/execute/stdin", content=body).status_code == 303
        report = client.get("/read/stdin").text
        result = "__NOT_PRINTED__"
        try:
            result = report.split("__start__", 1)[1].split("__end__", 1)[0]
        except:
            pass
        assert body in result
