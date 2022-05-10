
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
    print(args)
    code_inputs, code_outputs = execute(args.get("<file>"))
    produce_report(code_inputs, code_outputs)

if __name__ == "__main__":
    main()
