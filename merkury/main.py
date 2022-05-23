
"""merkury

Usage:
    merkury <file>

Options:
    -h --help     Show this screen.
    --version     Show version.
"""

from docopt import docopt
from .renderer import produce_report
from .runner import execute

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version="merkury 0.1")
    file_path = args.get("<file>")
    code = execute(file_path)
    file_name = file_path.split("/")[-1]
    produce_report(code, file_name)

if __name__ == "__main__":
    main()
