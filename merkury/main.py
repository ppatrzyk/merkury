
"""merkury

Usage:
    merkury [-o <file>] <script>

Options:
    -h --help                    Show this screen.
    -o <file>, --output <file>   Specify output file (if missing, prints to stdout)
    --version                    Show version.
"""

from docopt import docopt
from .renderer import produce_report
from .runner import execute

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version="merkury 0.2")
    python_file_path = args.get("<script>")
    output_file_path = args.get("--output")
    code = execute(python_file_path)
    produce_report(code, python_file_path, output_file_path)

if __name__ == "__main__":
    main()
