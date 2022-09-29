
"""merkury

Usage:
    merkury [-o <file>] [-f <format>] [-t <theme>] <script>

Options:
    -h --help                       Show this screen.
    -o <file>, --output <file>      Specify output file (if missing, "<script_name>_<date>").
    -f <format>, --format <format>  Specify format: html (default), pdf.
    -t <theme>, --theme <theme>     Specify color theme: dark (default), light. Valid for HTML output.
    -v, --version                   Show version.
"""

from .renderer import get_default_path, produce_report
from .runner import execute
from docopt import docopt
from pathlib import Path

FORMATS = ("html", "pdf", )
THEMES = ("dark", "light", )

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version="merkury 0.3")
    format = (args.get("--format") or "html").lower()
    assert format in FORMATS, f"Unknown format: {format}. Options: html, pdf"
    color_theme = (args.get("--theme") or "dark").lower()
    assert color_theme in THEMES, f"Unknown color theme: {color_theme}. Options: dark, light"
    python_file_path = Path(args.get("<script>"))
    output_file_path = Path(args.get("--output") or get_default_path(python_file_path, format))
    code = execute(python_file_path)
    produce_report(code, format, color_theme, python_file_path, output_file_path)

if __name__ == "__main__":
    main()
