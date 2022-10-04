
"""merkury

Usage:
    merkury [options] <script>

Options:
    -h --help                       Show this screen.
    -o <file>, --output <file>      Specify output file (if missing, "<script_name>_<date>").
    -f <format>, --format <format>  Specify format: html (default), pdf.
    -t <theme>, --theme <theme>     Specify color theme: dark (default), light. Valid for HTML output.
    -a <author>, --author <author>  Specify author (if missing, user name)
    -v, --version                   Show version.
"""

from .renderer import produce_report
from .runner import execute
from .utils import get_default_author, get_default_path
from docopt import docopt
from pathlib import Path

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
    author = (args.get("--author") or get_default_author())
    script_file_path = Path(args.get("<script>"))
    report_file_path = Path(args.get("--output") or get_default_path(script_file_path, format))
    code, duration = execute(script_file_path)
    produce_report(
        code=code,
        duration=duration,
        format=format,
        color_theme=color_theme,
        author=author,
        script_name=script_file_path.name,
        report_file_path=report_file_path
    )

if __name__ == "__main__":
    main()
