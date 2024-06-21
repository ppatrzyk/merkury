# Merkury

_Merkury_ is a command line utility to run Python scripts and render _static_ HTML or Markdown reports with code and produced output. It uses standard `.py` files as input - any valid script that can be run from command line, can also be turned into a report.

- [Example Python report](https://ppatrzyk.github.io/merkury/examples/intro-py.html)
- [Documentation](https://ppatrzyk.github.io/merkury/)

It's a lightweight alternative to tools such as [jupyter](https://github.com/jupyter/jupyter) and [papermill](https://github.com/nteract/papermill). While these have their advantages (and [problems](https://www.youtube.com/watch?v=7jiPeIFXb6U)), when everything you need is to generate a report from a data analysis script, they might be an overkill. This project is meant to address that scenario.

Non-goals of the project:

- interactive code execution in the browser (see [jupyter](https://github.com/jupyter/jupyter)),
- generating data apps that require backend server (see e.g. [dash](https://github.com/plotly/dash)),
- converting _any_ input into static HTML (see e.g. [nikola](https://github.com/getnikola/nikola)).

## Installation

```
pip3 install merkury
```

## Usage

```
$ merkury -h
merkury

Usage:
    merkury [options] <script>

Options:
    -h --help                       Show this screen.
    -o <file>, --output <file>      Specify report file (if missing, <script_name>_<date>).
    -f <format>, --format <format>  Specify report format: html (default), md.
    -a <author>, --author <author>  Specify author (if missing, user name).
    -t <title>, --title <title>     Specify report title (if missing, script file name)
    -c, --toc                       Generate Table of Contents
    -v, --version                   Show version and exit.
```

### PDF reports

It is also possible to obtain PDF reports with usage of additional conversion tools (e.g., [pandoc](https://github.com/jgm/pandoc)). For example:

```
merkury -o /dev/stdout -f md <your_script> | pandoc --highlight-style=tango -t pdf -o report.pdf
```

Note, in case your report file contains raw html chunks (such as plots or images), you will need use _wkhtmltopdf_ [pdf engine](https://pandoc.org/MANUAL.html#option--pdf-engine).

## Formatting and plots

In produced report, code will be broken into sections. Each section ends with a statement printing some output (e.g., `print()`). You can give titles to each section by placing _magic comment_ `#TITLE <your_section_title>` after line that produces output.

### Python

When it comes to report formatting, there are 3 types of outputs in a Python script: Standard `<code>` block (default), HTML, or Markdown.

By default _merkury_ treats any output as standard code print and puts it into `<code>` blocks. If your output is actually HTML or Markdown, you need to indicate that by placing a _magic comment_ after print statement in your script.

#### HTML

You need to put a comment `#HTML` after a line that outputs raw HTML. For example:

```
print(pandas_df.to_html(border=0))
#HTML
```

In addition to writing HTML by hand or using libraries that allow formatting output as HTML, _merkury_ provides [utility functions](merkury/utils.py) to format plots from common libraries. See [plotting docs](https://ppatrzyk.github.io/merkury/plotting.html) for details.

#### Markdown

It's also possible to render text formatted in markdown. You need to put magic comment `#MARKDOWN` after print statement.

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

- frontend: [pico](https://github.com/picocss/pico), [prism](https://github.com/PrismJS/prism), [tabler-icons](https://github.com/tabler/tabler-icons)
- [SO discussion that inspired this project](https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file)
- [pyreport](https://github.com/joblib/pyreport) - similar but long abandoned project
