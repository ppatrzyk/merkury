---
layout: default
title: Plotting
nav_order: 3
---

# Plotting
{: .no_toc }

In this section you can find description of tested libraries that are supported with merkury [utility functions](https://github.com/ppatrzyk/merkury/blob/master/merkury/utils.py). These are helper functions to format plot objects as HTML output.

In case you need to use something else: _any_ library that can produce plot in HTML format will work fine with _merkury_. For using PDF output it might be necessary that library is also able to produce images. Refer to [utility functions implementation](https://github.com/ppatrzyk/merkury/blob/master/merkury/utils.py) for examples how to achieve that.

1. TOC
{:toc}

## Output compatibility

Which plotting libraries you can use depening on desired output.

|                 | HTML     | PDF        | Notes                    |
| --------------- | -------- | ---------- | ------------------------ |
| **Altair**      | yes      | no         | requires _altair_saver_  |
| **Bokeh**       | yes      | no         |                          |
| **Matplotlib**  | yes      | yes        |                          |
| **Plotly**      | yes      | yes        | requires _kaleido_       |

## Altair

[Altair example](examples/altair.html)

```python
import altair as alt
from merkury.utils import output_altair

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
from merkury.utils import output_bokeh

plot = figure()
plot.circle([1, 2, 3, ], [3, 5, 4, ])

print(output_bokeh(plot))
#HTML
```

## Matplotlib

[Matplotlib example](examples/matplotlib.html)

```python
import matplotlib.pyplot as plt
from merkury.utils import output_matplotlib

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

print(output_matplotlib(fig))
#HTML
```

## Plotly

[Plotly example](examples/plotly.html)

```python
import plotly.graph_objs as go
from merkury.utils import output_plotly

data = [go.Scatter(
    x = [4, 5, 6, ],
    y = [78, 70, 74, ],
)]

fig = go.Figure(data=data)

print(output_plotly(fig))
#HTML
```
