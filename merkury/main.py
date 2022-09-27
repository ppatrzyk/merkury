
"""merkury

Usage:
    merkury [-o <file>] [-f <format>] <script>

Options:
    -h --help                       Show this screen.
    -o <file>, --output <file>      Specify output file (if missing, prints to stdout).
    -f <format>, --format <format>  Specify format: html (default), pdf.
    -v, --version                   Show version.
"""

from docopt import docopt
from .renderer import produce_report
from .runner import execute

FORMATS = ('html', 'pdf', )

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version="merkury 0.3")
    format = (args.get("--format") or 'html').lower()
    assert format in FORMATS, f'Unknown format: {format}. Options: html, pdf'
    python_file_path = args.get("<script>")
    output_file_path = args.get("--output")
    python_file_name = python_file_path.split("/")[-1]
    code = execute(python_file_path)
    produce_report(code, format, python_file_name, output_file_path)

if __name__ == "__main__":
    main()
