from merkury.plotting import (
    output_altair,
    output_bokeh,
    output_matplotlib,
    output_plotly,
    output_pyecharts,
)

intro = """
Examples how to include plots with different plotting libraries.
"""
print(intro)
#MARKDOWN

import altair as alt

print("## Altair")
#MARKDOWN

data = alt.Data(values=[{"x": 5, "y": 6}, {"x": 6, "y": 7}, {"x": 7, "y": 4}])
chart = alt.Chart(data).mark_point().encode(
    x="x:Q",
    y="y:Q",
)

print(output_altair(chart))
#HTML

from bokeh.plotting import figure

print("## Bokeh")
#MARKDOWN

plot = figure()
plot.scatter([1, 2, 3, ], [3, 5, 4, ])

print(output_bokeh(plot))
#HTML

import matplotlib.pyplot as plt

print("## Matplotlib")
#MARKDOWN

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 9, 16])

print(output_matplotlib(fig))
#HTML

import plotly.graph_objs as go

print("## Plotly")
#MARKDOWN

data = [go.Scatter(
    x = [4, 5, 6, ],
    y = [78, 70, 74, ],
)]

fig = go.Figure(data=data)

print(output_plotly(fig))
#HTML

from pyecharts.charts import Bar

print("## pyecharts")
#MARKDOWN

fig = Bar()
    
fig.add_xaxis(["A", "B", "C"])
fig.add_yaxis("Metric", [1, 3, 2])

print(output_pyecharts(fig))
#HTML