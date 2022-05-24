---
layout: default
title: Home
nav_order: 1
description: "Merkury is a simple tool to generate HTML reports from Python scripts"
permalink: /
---

# Merkury

_Merkury_ is a simple command line utility to run Python scripts and render _static_ HTML pages with code and produced output. It uses standard `.py` files as input - any valid Python script that can be run from command line, can also be turned into a HTML report.

It's a lightweight alternative to tools such as [jupyter](https://github.com/jupyter/jupyter) and [papermill](https://github.com/nteract/papermill). While these have their advantages (and [problems]((https://www.youtube.com/watch?v=7jiPeIFXb6U))), when everything you need is to generate a report from a python code run, they might be an overkill. This project is meant to address that scenario.

Please see an [example report](examples/intro.html) produced with it.

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
