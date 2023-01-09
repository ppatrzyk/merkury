
"""merkury

Usage:
    merkury [options] <script>

Options:
    -h --help                       Show this screen.
    -d <db>, --database <db>        Specify database location (if missing, in memory SQLite). Valid for SQL scripts.
    -o <file>, --output <file>      Specify report file (if missing, <script_name>_<date>).
    -f <format>, --format <format>  Specify report format: html (default), md.
    -a <author>, --author <author>  Specify author (if missing, user name).
    -t <title>, --title <title>     Specify report title (if missing, script file name)
    -i, --interactive               Make tables interactive (search, sort, paging). Valid for HTML output.
    -c, --toc                       Generate Table of Contents
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

FORMATS = ("html", "md", )
VERSION = version("merkury")

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version=f"merkury v{VERSION}")
    format = (args.get("--format") or "html").lower()
    assert format in FORMATS, f"Unknown format: {format}. Options: html, md"
    script_file_path = Path(args.get("<script>"))
    file_name = script_file_path.name
    start = time()
    match script_file_path.suffix.lower():
        case ".py":
            script_type = "python"
            code = execute_python(script_file_path)
        case ".sql":
            script_type = "SQL"
            db_path = args.get("--database") or ":memory:"
            code = execute_sql(db_path, script_file_path)
        case _:
            raise ValueError(f"Unknown file {script_file_path}")
    template_data = {
        "code": code,
        "duration": int(1000*(time()-start)),
        "format": format,
        "interactive": bool(args.get("--interactive")),
        "toc": bool(args.get("--toc")),
        "author": (args.get("--author") or getlogin()),
        "script_type": script_type,
        "title": args.get("--title") or file_name,
        "file_name": file_name,
        "report_file_path": Path(args.get("--output") or get_default_path(script_file_path, format)),
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "version": VERSION,
    }
    produce_report(template_data)

if __name__ == "__main__":
    main()
