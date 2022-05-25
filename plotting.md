---
layout: default
title: Plotting
nav_order: 3
---

# Plotting
{: .no_toc }

_Any_ library that can produce plot in HTML format will work fine with _Merkury_. Below are examples on how to achieve that with some of them.

1. TOC
{:toc}

## Altair

[Save chart as html](https://altair-viz.github.io/user_guide/saving_charts.html) and print contents of the file.

```python
import os
import tempfile
import altair as alt

data = alt.Data(values=[{"x": 5, "y": 6}, {"x": 6, "y": 7}, {"x": 7, "y": 4}])
chart = alt.Chart(data).mark_point().encode(
    x="x:Q",
    y="y:Q",
)

temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
chart.save(temp.name)

with open(temp.name, "r") as f:
    rendered_chart = f.read()
    print(rendered_chart)
#HTML

os.remove(temp.name)
```

- [Altair example](examples/altair.html)

## Bokeh

Print output of [`file_html`](https://docs.bokeh.org/en/latest/docs/user_guide/embed.html#userguide-embed-standalone).

```python
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

plot = figure()
plot.circle([1, 2, 3, ], [3, 5, 4, ])

html = file_html(plot, CDN, "Bokeh plot")
print(html)
#HTML
```

- [Bokeh example](examples/bokeh.html)

## Matplotlib

You need to export figure to html using [`mpld3`](https://mpld3.github.io/modules/API.html#mpld3.fig_to_html).

```python
import matplotlib.pyplot as plt
import mpld3

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

html = mpld3.fig_to_html(fig)
print(html)
#HTML
```

- [Matplotlib example](examples/matplotlib.html)

## Plotly

```python
import plotly
import plotly.graph_objs as go

data = [go.Scatter(
    x = [4, 5, 6, ],
    y = [78, 70, 74, ],
)]

fig = go.Figure(data=data)

print(plotly.io.to_html(fig, include_plotlyjs="cdn"))
#HTML
```

Print output of [`plotly.io.to_html`](https://plotly.com/python-api-reference/generated/plotly.io.to_html.html). Please refer to plotly docs on different options how to provide javascript dependencies.

- [Plotly example](examples/plotly.html)
