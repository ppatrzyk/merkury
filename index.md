---
layout: default
title: Home
nav_order: 1
description: "Merkury is a simple tool to generate HTML reports from Python scripts"
permalink: /
---

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

## Acknowledgements

- Reports styling is made possible by great frontend libs [pico](https://github.com/picocss/pico), [prism](https://github.com/PrismJS/prism), and [list.js](https://github.com/javve/list.js)
- [SO discussion that inspired this project](https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file)
- [pyreport](https://github.com/joblib/pyreport) - similar but long abandoned project
