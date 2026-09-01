"""
Utility functions
"""

import re
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

FORMATS = (
    "html",
    "md",
)
VERSION = version("merkury")


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


def get_python_files(path: Path) -> tuple[Path]:
    """
    List python files inside directory
    """
    return tuple(
        sorted(
            found_path
            for found_path in path.rglob("*")
            if (found_path.is_file() and found_path.suffix.lower() == ".py")
        )
    )
