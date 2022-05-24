# Merkury

_Merkury_ is a simple command line utility to run Python scripts and render _static_ HTML pages with code and produced output. It uses standard `.py` files as input - any valid Python script that can be run from command line, can also be turned into a HTML report.

It's a lightweight alternative to tools such as [jupyter](https://github.com/jupyter/jupyter) and [papermill](https://github.com/nteract/papermill). While these have their advantages (and [problems](https://www.youtube.com/watch?v=7jiPeIFXb6U)), when everything you need is to generate a report from a python code run, they might be an overkill. This project is meant to address that scenario.

- [Example report produced with merkury](https://ppatrzyk.github.io/merkury/examples/intro.html)
- [Docs page](https://ppatrzyk.github.io/merkury/)

Non-goals of the project:

- interactive code execution in the browser (see [jupyter](https://github.com/jupyter/jupyter)),
- generating data apps that require backend server (see e.g. [dash](https://github.com/plotly/dash)),
- converting _any_ input into static HTML (see e.g. [nikola](https://github.com/getnikola/nikola)).

_NOTE: this is an early experimental project, stuff might break and change_

## Installation

```
pip3 install merkury
```

## Usage

```
$ merkury -h
merkury

Usage:
    merkury [-o <file>] <script>

Options:
    -h --help                    Show this screen.
    -o <file>, --output <file>   Specify output file (if missing, prints to stdout)
    --version                    Show version.
```

By default `merkury` prints HTML output to stdout:

```
merkury myscript.py > myscript.html
```

Alternatively, you can specify output file as a parameter:

```
merkury -o myscript.html myscript.py
```

## Formatting and plots

By default merkury treats any output as simple print and puts it into `<code>` blocks. There is also a possibility to treat it as either raw HTML or markdown. This is achieved by placing a _magic comment_ after print statement in your script.

### HTML

You need to put a comment `#HTML` after a line that outputs raw HTML.

Example:

```
print("""<img src="https://www.python.org/static/img/python-logo-large.c36dccadd999.png" alt="python">""")
#HTML
```

Using raw HTML provides a way to include **plots** in your reports. Please see [documentation]() for details.

### Markdown

It's also possible to print markdown text and have it rendered to html by `merkury`. You need to put magic comment `#MARKDOWN` after print statement.

For example:

```
print("""
# I'm a markdown header

List:

* l1
* l2

""")
#MARKDOWN
```

## Acknowledgements

- [SO discussion that inspired this project](https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file)
- [pyreport](https://github.com/joblib/pyreport) - similar but long abandoned project
