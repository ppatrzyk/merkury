---
layout: default
title: Home
nav_order: 1
description: "Merkury is a simple tool to generate HTML reports from Python scripts"
permalink: /
---

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

## Acknowledgements

- Reports styling is made possible by great frontend libs [pico](https://github.com/picocss/pico) and [prism](https://github.com/PrismJS/prism)
- [SO discussion that inspired this project](https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file)
- [pyreport](https://github.com/joblib/pyreport) - similar but long abandoned project
