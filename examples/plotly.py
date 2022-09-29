import plotly.graph_objs as go
from merkury.utils import output_plotly

intro = """
# Plotly usage

Example of how to include plotly plots in merkury HTML reports.
"""
print(intro)
#MARKDOWN

data = [go.Scatter(
    x = [4, 5, 6, ],
    y = [78, 70, 74, ],
)]

fig = go.Figure(data=data)

print(output_plotly(fig))
#HTML

print(output_plotly(fig, interactive=False))
#HTML
