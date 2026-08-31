import logging
from pathlib import Path

import uvicorn
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from starlette.routing import Route

from .runner_py import get_report
from .utils import get_report_path

logger = logging.getLogger(__name__)


async def execute(request: Request):
    script = request.path_params["script"]
    script_path = request.app.state.script_mapping.get(script, None)
    if (script_path is None) or (not script_path.is_file()):
        raise HTTPException(status_code=404, detail="Script not found")
    report_file_path = get_report_path(
        script_path, request.app.state.specified_output, "html", False
    )
    logger.debug(f"executes {script_path}, will write to {report_file_path}")
    get_report(script_path, report_file_path, request.app.state.template_data)
    return RedirectResponse(
        url=request.app.url_path_for("read", script=script), status_code=303
    )


async def read(request: Request):
    script = request.path_params["script"]
    report_file_path = Path(request.app.state.specified_output, f"{script}.html")
    logger.debug(f"reading from {report_file_path}")
    if not report_file_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(
        path=report_file_path,
        media_type="text/html",
        headers={"cache-control": "no-cache"},
    )


routes = [
    Route("/execute/{script:str}", execute),
    Route("/read/{script:str}", read),
]


def _get_app(
    sub_paths: tuple[Path], specified_output: Path, template_data: dict
) -> Starlette:
    """
    Generate starlette app
    """
    app = Starlette(debug=True, routes=routes)
    app.state.specified_output = specified_output
    app.state.template_data = template_data
    app.state.script_mapping = {sub_path.stem: sub_path for sub_path in sub_paths}
    return app


def run_server(
    server_host: str,
    server_port: int,
    sub_paths: tuple[Path],
    specified_output: Path,
    template_data: dict,
):
    """
    Run server
    """
    if specified_output is None:
        specified_output = Path("server_reports")
        specified_output.mkdir(parents=True, exist_ok=True)
    else:
        assert specified_output.is_dir(), "output location must be existing directory"
    app = _get_app(sub_paths, specified_output, template_data)
    uvicorn.run(
        app=app,
        host=server_host,
        port=server_port,
        log_level="info",
    )
