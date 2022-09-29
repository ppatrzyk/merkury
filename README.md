# Merkury

_Merkury_ is a command line utility to run Python scripts and render _static_ HTML or PDF reports with code and produced output. It uses standard `.py` files as input - any valid Python script that can be run from command line, can also be turned into a report.

- [Example report](https://ppatrzyk.github.io/merkury/examples/intro.html)
- [Docs page](https://ppatrzyk.github.io/merkury/)

It's a lightweight alternative to tools such as [jupyter](https://github.com/jupyter/jupyter) and [papermill](https://github.com/nteract/papermill). While these have their advantages (and [problems](https://www.youtube.com/watch?v=7jiPeIFXb6U)), when everything you need is to generate a report from a python code run, they might be an overkill. This project is meant to address that scenario.

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
    merkury [-o <file>] [-f <format>] [-t <theme>] <script>

Options:
    -h --help                       Show this screen.
    -o <file>, --output <file>      Specify output file (if missing, "<script_name>_<date>").
    -f <format>, --format <format>  Specify format: html (default), pdf.
    -t <theme>, --theme <theme>     Specify color theme: dark (default), light. Valid for HTML output.
    -v, --version                   Show version.
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

In addition to writing HTML by hand or using libraries that allow formatting output as HTML, `merkury` provides [utility functions](merkury/utils.py) to format **plots** from common libraries. See [plotting docs](https://ppatrzyk.github.io/merkury/plotting.html) for details.

### Markdown

It's also possible to print text formatted in markdown. You need to put magic comment `#MARKDOWN` after print statement.

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

- Reports styling is made possible by great frontend libs [pico](https://github.com/picocss/pico) and [prism](https://github.com/PrismJS/prism)
- [SO discussion that inspired this project](https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file)
- [pyreport](https://github.com/joblib/pyreport) - similar but long abandoned project
