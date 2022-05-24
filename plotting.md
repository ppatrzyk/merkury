---
layout: default
title: Plotting
nav_order: 3
---

# Plotting
{: .no_toc }

_Any_ library that can produce plot in HTML format will work fine with Merkury. Below are examples on how to achieve that with some of them.

1. TOC
{:toc}

## Altair

[Save chart as html](https://altair-viz.github.io/user_guide/saving_charts.html) and print contents of the file.

- [Example Merkury report](examples/altair.html)

## Bokeh

Print output of [`file_html`](https://docs.bokeh.org/en/latest/docs/user_guide/embed.html#userguide-embed-standalone).

- [Example Merkury report](examples/bokeh.html)

## Matplotlib

You need to export figure to html using [`mpld3`](https://mpld3.github.io/modules/API.html#mpld3.fig_to_html).

- [Example Merkury report](examples/matplotlib.html)

## Plotly

Print output of [`plotly.io.to_html`](https://plotly.com/python-api-reference/generated/plotly.io.to_html.html). Please refer to plotly docs on different options how to provide javascript dependencies.

- [Example Merkury report](examples/plotly.html)
