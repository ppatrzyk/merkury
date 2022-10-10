# Merkury

_Merkury_ is a command line utility to run Python and SQL scripts and render _static_ HTML or PDF reports with code and produced output. It uses standard `.py` or `.sql` files as input - any valid script that can be run from command line, can also be turned into a report.

- [Example Python report](https://ppatrzyk.github.io/merkury/examples/intro-py.html)
- [Example SQL report](https://ppatrzyk.github.io/merkury/examples/intro-sql.html)
- [Documentation](https://ppatrzyk.github.io/merkury/)

It's a lightweight alternative to tools such as [jupyter](https://github.com/jupyter/jupyter) and [papermill](https://github.com/nteract/papermill). While these have their advantages (and [problems](https://www.youtube.com/watch?v=7jiPeIFXb6U)), when everything you need is to generate a report from a data analysis script, they might be an overkill. This project is meant to address that scenario.

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
    merkury [options] <script>

Options:
    -h --help                       Show this screen.
    -d <db>, --database <db>        Specify database location (if missing, in memory SQLite). Valid for SQL scripts.
    -o <file>, --output <file>      Specify report file (if missing, "<script_name>_<date>").
    -f <format>, --format <format>  Specify report format: html (default), pdf.
    -t <theme>, --theme <theme>     Specify report color theme: dark (default), light. Valid for HTML output.
    -i, --interactive               Make tables interactive (search, sort, paging). Valid for HTML output.
    -a <author>, --author <author>  Specify author (if missing, user name)
    -v, --version                   Show version and exit.
```

### Database connection

For running SQL scripts, _merkury_ supports PostgreSQL and SQLite. Regarding `--database` option:

- For SQLite, you need to specify path to db file (or empty if you want to run script in memory without an existing db)
- For PostgreSQL, you need to specify [connection string](https://www.postgresql.org/docs/current/libpq-connect.html#id-1.7.3.8.3.6), i.e.: `postgresql://[userspec@][hostspec][/dbname][?paramspec]`

### Automatic interactive tables

When setting `--interactive ` option, _merkury_ will try to make all HTML `<table>` elements in the report interactive (i.e. add search, sort, and pagination). It's always safe to use with SQL scripts, for Python you need to ensure that printed table uses proper elements (i.e. `<th>` indicating headers rather that data cells). If this is not the case, interactive elements will not function properly.

## Formatting and plots

### Python

When it comes to report formatting, there are 3 types of outputs in a Python script: Standard `<code>` block (default), HTML, or Markdown.

By default _merkury_ treats any code printing some output (e.g., `print()`) as one containing code and puts it into `<code>` blocks. If your output is actually HTML or Markdown, you need to indicate that by placing a _magic comment_ after print statement in your script.

#### HTML

You need to put a comment `#HTML` after a line that outputs raw HTML. For example:

```
print(pandas_df.to_html(border=0))
#HTML
```

In addition to writing HTML by hand or using libraries that allow formatting output as HTML, _merkury_ provides [utility functions](merkury/utils.py) to format **plots** from common libraries. See [plotting docs](https://ppatrzyk.github.io/merkury/plotting.html) for details.

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

### SQL

Unlike Python, there are no special formatting instructions you can specify in comments. Outputs from all queries will be formatted as a HTML table.

## Acknowledgements

- Reports styling is made possible by great frontend libs [pico](https://github.com/picocss/pico), [prism](https://github.com/PrismJS/prism), and [list.js](https://github.com/javve/list.js)
- [SO discussion that inspired this project](https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file)
- [pyreport](https://github.com/joblib/pyreport) - similar but long abandoned project
