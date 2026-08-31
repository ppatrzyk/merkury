"""
Utility functions for code output formatting
"""

import base64
import io
import os
import re
import tempfile
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

FORMATS = (
    "html",
    "md",
)
VERSION = version("merkury")

### Helpers for Plotting ###


def output_altair(figure):
    """
    Process altair figure
    """
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    figure.save(temp.name)
    with open(temp.name, "r") as f:
        rendered_figure = f.read()
    os.remove(temp.name)
    return rendered_figure


def output_bokeh(figure):
    """
    Process boheh figure
    """
    from bokeh.embed import file_html
    from bokeh.resources import CDN

    return file_html(figure, CDN, "Bokeh plot")


def output_matplotlib(figure):
    """
    Process matplotlib figure
    """
    fig_bytes = io.BytesIO()
    figure.savefig(fig_bytes, format="png")
    fig_bytes.seek(0)
    return _bytes_to_html(fig_bytes.read())


def output_plotly(figure, interactive=True):
    """
    Process plotly figure
    """
    import plotly

    if interactive:
        return plotly.io.to_html(figure, include_plotlyjs="cdn")
    else:
        img_bytes = figure.to_image(format="png")
        return _bytes_to_html(img_bytes)


def _bytes_to_html(bytes):
    """
    Helper for getting base64 encoded img html tag
    """
    img_encoded = base64.b64encode(bytes).decode()
    img_html = f"""<img src="data:image/png;base64,{img_encoded}" />"""
    return img_html


# TODO making altair and bokeh charts non-interactive (png)
# for pdfs possible, but would require js dependencies see
# https://pypi.org/project/altair-saver/
# https://docs.bokeh.org/en/latest/docs/user_guide/export.html#additional-dependencies

### Other utils ###


def _get_default_file_name(
    script_file_path: Path, output_format: str, include_date: bool
) -> str:
    """
    Default file name
    """
    file_name = re.sub(r"\.py$", "", script_file_path.name)
    if include_date:
        date_now = datetime.now().astimezone().strftime("%Y%m%d%H%M%S%Z")
        out_file_name = f"{file_name}_{date_now}.{output_format}"
    else:
        out_file_name = f"{file_name}.{output_format}"
    return out_file_name


def _get_default_path(
    script_file_path: Path, output_format: str, include_date: bool
) -> Path:
    """
    Default file path for report
    """
    out_file_name = _get_default_file_name(
        script_file_path, output_format, include_date
    )
    return Path(script_file_path.parent, out_file_name)


def process_output_path(specified_output: str | None) -> Path | None:
    """
    Process output path specified in script
    """
    # no need to touch file in default case because its written to same dir as script
    if specified_output is not None:
        specified_output = Path(specified_output).resolve()
        if not specified_output.exists():
            if specified_output.suffix.lower().strip(".") in FORMATS:
                specified_output.parent.mkdir(parents=True, exist_ok=True)
                specified_output.touch()
            else:
                specified_output.mkdir(parents=True, exist_ok=True)
    return specified_output


def get_report_path(
    script_file_path: Path,
    specified_output: Path | None,
    output_format: str,
    include_date: bool,
) -> Path:
    """
    Get report path
    """
    if specified_output is None:
        report_file_path = _get_default_path(
            script_file_path, output_format, include_date
        )
    else:
        if specified_output.is_dir():
            file_name = _get_default_file_name(
                script_file_path, output_format, include_date
            )
            report_file_path = Path(specified_output, file_name)
        else:
            report_file_path = specified_output  # /dev/null etc cases
    return report_file_path
