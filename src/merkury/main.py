
"""merkury

Usage:
    merkury [options] <script>

Options:
    -h --help                       Show this screen.
    -o <file>, --output <file>      Specify report file (if missing, <script_name>_<date>).
    -f <format>, --format <format>  Specify report format: html (default), md.
    -a <author>, --author <author>  Specify author (if missing, user name).
    -t <title>, --title <title>     Specify report title (if missing, script file name).
    -i, --no-input                  Hide input blocks in generated report.
    -c, --toc                       Generate Table of Contents.
    -d, --debug                     Print debug messages.
    -v, --version                   Show version and exit.

Source:
    https://github.com/ppatrzyk/merkury
"""

import logging
from .renderer import generate_report
from .runner_py import execute_python
from .utils import get_default_path, VERSION

from docopt import docopt
from os import getlogin
from pathlib import Path

FORMATS = ("html", "md", )

def get_report(script_file_path: Path, report_file_path: Path, template_data: dict) -> bool:
    duration_ms, code = execute_python(script_file_path)
    template_data = {
        **template_data,
        "duration_ms": duration_ms,
        "file_name": script_file_path.name,
    }
    generate_report(code, report_file_path, template_data)
    return True

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version=f"merkury v{VERSION}")
    if bool(args.get("--debug")):
        logging.basicConfig(level=logging.DEBUG)
    output_format = (args.get("--format") or "html").lower()
    assert output_format in FORMATS, f"Unknown format: {output_format}. Options: html, md"
    script_file_path: Path = Path(args.get("<script>"))
    file_name = script_file_path.name
    assert script_file_path.suffix.lower() == ".py", f"Unknown file {script_file_path}"
    report_file_path = Path(args.get("--output") or get_default_path(script_file_path, output_format))
    template_data = {
        "output_format": output_format,
        "show_input_blocks": not bool(args.get("--no-input")),
        "toc": bool(args.get("--toc")),
        "author": (args.get("--author") or getlogin()),
        "title": args.get("--title") or script_file_path.name,
    }
    get_report(script_file_path, report_file_path, template_data)

if __name__ == "__main__":
    main()
