
"""merkury

Usage:
    merkury [options] <script>

Options:
    -h --help                       Show this screen.
    -d <db>, --database <db>        Specify database location (if missing, in memory SQLite). Valid for SQL scripts.
    -o <file>, --output <file>      Specify report file (if missing, "<script_name>_<date>").
    -f <format>, --format <format>  Specify report format: html (default), pdf.
    -t <theme>, --theme <theme>     Specify report color theme: dark (default), light. Valid for HTML output.
    -i, --interactive               Make tables interactive (search, sort, paging). Valid for HTML output.
    -a <author>, --author <author>  Specify author (if missing, user name)
    -v, --version                   Show version and exit.
"""

from .renderer import produce_report
from .runner_py import execute_python
from .runner_sql import execute_sql
from .utils import get_default_path
from datetime import datetime
from importlib.metadata import version
from docopt import docopt
from os import getlogin
from pathlib import Path
from time import time

FORMATS = ("html", "pdf", )
THEMES = ("dark", "light", )
VERSION = version("merkury")

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version=f"merkury v{VERSION}")
    format = (args.get("--format") or "html").lower()
    assert format in FORMATS, f"Unknown format: {format}. Options: html, pdf"
    color_theme = "light" if (format == "pdf") else ((args.get("--theme") or "dark").lower())
    assert color_theme in THEMES, f"Unknown color theme: {color_theme}. Options: dark, light"
    script_file_path = Path(args.get("<script>"))
    report_file_path = Path(args.get("--output") or get_default_path(script_file_path, format))
    script_type = script_file_path.suffix.lower()
    start = time()
    match script_type:
        case ".py":
            code = execute_python(script_file_path)
        case ".sql":
            db_path = args.get("--database") or ":memory:"
            code = execute_sql(db_path, script_file_path)
        case _:
            raise ValueError(f"Unknown file {script_file_path}")
    template_data = {
        "duration": int(1000*(time()-start)),
        "format": format,
        "color_theme": color_theme,
        "interactive": bool(args.get("--interactive")),
        "author": (args.get("--author") or getlogin()),
        "script_type": script_type,
        "file_name": script_file_path.name,
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "version": VERSION,
    }
    produce_report(
        code=code,
        report_file_path=report_file_path,
        template_data=template_data
    )

if __name__ == "__main__":
    main()
