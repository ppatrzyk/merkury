---
layout: default
title: Plotting
nav_order: 3
---

# Plotting
{: .no_toc }

In this section you can find description of tested libraries that are supported with merkury [utility functions](https://github.com/ppatrzyk/merkury/blob/master/merkury/utils.py). In case you need to use something else: _any_ library that can produce plot in HTML format will work fine with _merkury_ when producing HTML report. For PDF reports it's necessary that library is able to produce images. Refer to [utility functions implementation](https://github.com/ppatrzyk/merkury/blob/master/merkury/utils.py) how to achieve that.

1. TOC
{:toc}

## Output compatibility

|                 | HTML     | PDF        | Notes                    |
| --------------- | -------- | ---------- | ------------------------ |
| **Altair**      | yes      | no         | requires _altair_saver_  |
| **Bokeh**       | yes      | no         |                          |
| **Matplotlib**  | yes      | yes        |                          |
| **Plotly**      | yes      | yes        | requires _kaleido_       |

## Altair

[Altair example](examples/altair.html)

```python
import os
import tempfile
import altair as alt

data = alt.Data(values=[{"x": 5, "y": 6}, {"x": 6, "y": 7}, {"x": 7, "y": 4}])
chart = alt.Chart(data).mark_point().encode(
    x="x:Q",
    y="y:Q",
)

print(output_altair(chart))
#HTML

```

## Bokeh

[Bokeh example](examples/bokeh.html)

```python
from bokeh.plotting import figure

plot = figure()
plot.circle([1, 2, 3, ], [3, 5, 4, ])

print(output_bokeh(plot))
#HTML
```

## Matplotlib

[Matplotlib example](examples/matplotlib.html)

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

print(output_matplotlib(fig))
#HTML
```

## Plotly

[Plotly example](examples/plotly.html)

```python
import plotly
import plotly.graph_objs as go

data = [go.Scatter(
    x = [4, 5, 6, ],
    y = [78, 70, 74, ],
)]

fig = go.Figure(data=data)

print(output_plotly(fig))
#HTML

print(output_plotly(fig, interactive=False))
#HTML
```
