
"""merkury

Usage:
    merkury <file>

Options:
    -h --help     Show this screen.
    --version     Show version.
"""

from docopt import docopt
from .runner import execute

def main():
    """
    Program entrypoint
    """
    args = docopt(__doc__, version="merkury 0.1")
    print(args)
    output = execute(args.get("<file>"))

if __name__ == "__main__":
    main()
