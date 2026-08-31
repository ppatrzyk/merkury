from pathlib import Path

import uvicorn
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.routing import Route

from .runner_py import get_report
from .utils import get_report_path


async def execute(request: Request):
    script = request.path_params["script"]
    script_path = app.state.script_mapping.get(script, None)
    if (script_path is None) or (not script_path.is_file()):
        raise HTTPException(status_code=404, detail="Script not found")
    report_file_path = get_report_path(
        script_path, app.state.specified_output, "html", False
    )
    get_report(script_path, report_file_path, app.state.template_data)
    return RedirectResponse(
        url=request.app.url_path_for("read", script=script), status_code=303
    )


async def read(request: Request):
    script = request.path_params["script"]
    report_path = Path(app.state.specified_output, f"{script}.html")
    if not report_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(
        path=report_path,
        media_type="text/html",
        headers={"cache-control": "no-cache"},
    )


routes = [
    Route("/execute/{script:str}", execute),
    Route("/read/{script:str}", read),
]

app = Starlette(debug=True, routes=routes)


def run_server(sub_paths: tuple[Path], specified_output: Path, template_data: dict):
    """
    Generate app and start server
    """
    if specified_output is None:
        specified_output = Path("server_reports")
        specified_output.mkdir(parents=True, exist_ok=True)
    else:
        assert specified_output.is_dir(), "output location must be existing directory"
    app.state.specified_output = specified_output
    app.state.template_data = template_data
    app.state.script_mapping = {sub_path.stem: sub_path for sub_path in sub_paths}
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
    )
