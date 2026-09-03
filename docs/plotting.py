from merkury.plotting import (
    output_altair,
    output_bokeh,
    output_matplotlib,
    output_plotly,
    output_pyecharts,
)

intro = """
Examples how to include plots with different plotting libraries.

Libraries that produce interactive, Javascript-based plots work only with _html_ output format. 
For _markdown_, produce static plot images (e.g., with _matplotlib_).
"""
print(intro)
#TITLE Plotting
#MARKDOWN

import altair as alt

data = alt.Data(values=[{"x": 5, "y": 6}, {"x": 6, "y": 7}, {"x": 7, "y": 4}])
chart = alt.Chart(data).mark_point().encode(
    x="x:Q",
    y="y:Q",
)

output_altair(chart)
#TITLE Altair
#HTML

from bokeh.plotting import figure

plot = figure()
plot.scatter([1, 2, 3, ], [3, 5, 4, ])

output_bokeh(plot)
#TITLE Bokeh
#HTML

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

output_matplotlib(fig)
#TITLE Matplotlib
#HTML

import plotly.graph_objs as go

data = [go.Scatter(
    x = [4, 5, 6, ],
    y = [78, 70, 74, ],
)]

fig = go.Figure(data=data)

output_plotly(fig)
#TITLE Plotly
#HTML

from pyecharts.charts import Bar

fig = Bar()
    
fig.add_xaxis(["A", "B", "C"])
fig.add_yaxis("Metric", [1, 3, 2])

output_pyecharts(fig)
#TITLE Pyecharts
#HTML