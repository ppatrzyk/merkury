# Merkury

_Merkury_ is a command line utility to run Python scripts and render _static_ HTML or Markdown reports. It uses standard `.py` files as input - any valid script that can be run from command line, can also be turned into a report.

It's a lightweight alternative to tools such as [jupyter](https://github.com/jupyter/jupyter)/[papermill](https://github.com/nteract/papermill) and can be used as a _BI-as-code_ solution with Python-based workflow.

- [Documentation](https://ppatrzyk.github.io/merkury/)
- [Example report](https://ppatrzyk.github.io/merkury/intro-py.html)
- [Plotting examples](https://ppatrzyk.github.io/merkury/plotting.html)

Non-goals of the project:

- interactive code execution in the browser (see [jupyter](https://github.com/jupyter/jupyter)),
- generating data apps that require backend server (see e.g. [dash](https://github.com/plotly/dash)),
- converting _any_ input into static HTML (see e.g. [nikola](https://github.com/getnikola/nikola)).

## Installation

```bash
pip3 install merkury

# if you also need server mode
pip3 install merkury[server]
```

There is also docker image available:

```bash
# default command runs in server mode
podman run \
    --rm \
    -p 8000:8000 \
    -v path/to/script/dir:/etc/merkury/scripts \
    ghcr.io/ppatrzyk/merkury:0.14
```

## Usage

Merkury can run in the following modes:

### Single file

```bash
merkury -f html -o report.html myscript.py
```

### Batch

Runs concurrently all python scripts inside given directory and produces report for each one.

```bash
merkury -f html -o path/to/reports batch path/to/scripts
```

### Server

Starts server that exposes execution endpoints for each script in provided directory.

```bash
merkury -s localhost:8000 server path/to/scripts
```

With this configuration, there is:

- Homepage with script list at [/](http://localhost:8000/),
- For each script (e.g., `s.py`):
    - Execution endpoint to run it (and refresh report html) at [/execute/s](http://localhost:8000/execute/s),
    - Report endpoint to view latest report at [/read/s](http://localhost:8000/read/s).

Arguments to script can be passed via query params. Calling [/execute/s?arg=mycommand&arg=123](http://localhost:8000/execute/s?arg=mycommand&arg=123) is equivalent to running `python3 s.py mycommand 123`.

If a script reads data from _stdin_, it can be passed via body in POST request:

```bash
curl \
    -X POST \
    -d 'in data' \
    http://localhost:8000/execute/s
```

## Options

```bash
$ merkury -h
merkury

Usage:
    merkury [options] server <dir_path>
    merkury [options] batch <dir_path> [ARGS...]
    merkury [options] <script_path> [ARGS...]

Options:
    -h --help                         Show this screen.
    -o <file>, --output <file>        Specify report file (if missing, <script_name>.<format>).
    -f <format>, --format <format>    Specify report format: html (default), md.
    -a <author>, --author <author>    Specify author (if missing, user name).
    -t <title>, --title <title>       Specify report title (if missing, script file name).
    -p <count>, --parallel <count>    Parallel processes (if missing, cpu cores).
    -s <address>, --server <address>  Server address (if missing, localhost:8000).
    -d, --timestamp                   Add timestamp to default report file name.
    -i, --no-input                    Hide input blocks in generated report.
    -c, --toc                         Generate Table of Contents.
    -l, --debug                       Print debug messages.
    -v, --version                     Show version and exit.

Source:
    https://github.com/ppatrzyk/merkury
```

## Formatting

Formatting of output inside report is controlled by inserting _magic comments_ inside input script. There are following optional directives:

- [`#HTML`](#html)
- [`#MARKDOWN`](markdown)
- [`#TITLE`](#title)

By default _merkury_ treats any output as standard code print and puts it into `<code>` blocks. Only If your output is actually HTML or Markdown, you need to indicate that by placing a _magic comment_ inside a code chunk.

### HTML

You need to put a comment `#HTML` after a line that outputs raw HTML. For example:

```python
print(pandas_df.to_html(border=0))
# HTML
```

In addition to writing HTML by hand or using libraries that allow formatting output as HTML, _merkury_ provides [utility functions](https://github.com/ppatrzyk/merkury/blob/master/src/merkury/plotting.py) to format plots from common libraries. See [plotting docs](https://ppatrzyk.github.io/merkury/plotting.html) for details.

### Markdown

It's also possible to render text formatted in markdown. You need to put magic comment `#MARKDOWN` after print statement.

For example:

```python
print("""
# I'm a markdown header

List:

* l1
* l2

""")
# MARKDOWN
```

### Title

In produced report, code will be broken into sections. Each section ends with a statement printing some output (e.g., `print()`). You can optionally give titles to each section by placing _magic comment_ `#TITLE <your_section_title>` inside code chunk.

## PDF reports

It is also possible to obtain PDF reports with usage of additional conversion tools (e.g., [pandoc](https://github.com/jgm/pandoc)). For example:

```bash
merkury -o /dev/stdout -f md <your_script> | pandoc --highlight-style=tango -t pdf -o report.pdf
```

Note, in case your report file contains raw html chunks (such as plots or images), you will need use _wkhtmltopdf_ [pdf engine](https://pandoc.org/MANUAL.html#option--pdf-engine).

## DEV

dev installation:

```bash
pip3 install -e .[dev,server]
```

docker build:

```bash
podman build -t ghcr.io/ppatrzyk/merkury:0.14 .
```

docs:

```bash
merkury --no-input docs/index.py
merkury --toc docs/intro-py.py
merkury docs/plotting.py
```

## Acknowledgements

- [SO discussion that inspired this project](https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file)
- [pyreport](https://github.com/joblib/pyreport) - similar but long abandoned project
- frontend: [pico](https://github.com/picocss/pico), [prism](https://github.com/PrismJS/prism), [tabler-icons](https://github.com/tabler/tabler-icons)
