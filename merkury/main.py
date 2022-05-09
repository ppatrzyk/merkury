
"""merkury

Usage:
    merkury <file>

Options:
    -h --help     Show this screen.
    --version     Show version.
"""

from docopt import docopt

def main():
    args = docopt(__doc__, version="merkury 0.1")
    print(args)

if __name__ == "__main__":
    main()
