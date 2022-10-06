
"""merkury

Usage:
    merkury [options] <script>

Options:
    -h --help                       Show this screen.
    -d <db>, --database <db>        Specify database file path (if missing, in memory). Valid for SQL scripts.
    -o <file>, --output <file>      Specify report file (if missing, "<script_name>_<date>").
    -f <format>, --format <format>  Specify report format: html (default), pdf.
    -t <theme>, --theme <theme>     Specify report color theme: dark (default), light. Valid for HTML output.
    -a <author>, --author <author>  Specify author (if missing, user name)
    -v, --version                   Show version and exit.
"""

from .renderer import produce_report
from .runner_py import execute_python
from .runner_sql import execute_sqlite
from .utils import get_default_path
from docopt import docopt
from os import getlogin
from pathlib import Path
from time import time

FORMATS = ("html", "pdf", )
THEMES = ("dark", "light", )

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version="merkury v0.4")
    format = (args.get("--format") or "html").lower()
    assert format in FORMATS, f"Unknown format: {format}. Options: html, pdf"
    color_theme = (args.get("--theme") or "dark").lower()
    assert color_theme in THEMES, f"Unknown color theme: {color_theme}. Options: dark, light"
    author = (args.get("--author") or getlogin())
    script_file_path = Path(args.get("<script>"))
    report_file_path = Path(args.get("--output") or get_default_path(script_file_path, format))
    start = time()
    match script_file_path.suffix.lower():
        case ".py":
            code = execute_python(script_file_path)
        case ".sql":
            db_path = args.get("--database") or ":memory:"
            code = execute_sqlite(db_path, script_file_path)
        case _:
            raise ValueError(f"Unknown file {script_file_path}")
    duration_ms = int(1000*(time()-start))
    produce_report(
        code=code,
        duration=duration_ms,
        format=format,
        color_theme=color_theme,
        author=author,
        script_name=script_file_path.name,
        report_file_path=report_file_path
    )

if __name__ == "__main__":
    main()
