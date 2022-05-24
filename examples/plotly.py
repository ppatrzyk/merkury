import plotly
import plotly.graph_objs as go

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

print(plotly.io.to_html(fig, include_plotlyjs="cdn"))
#HTML
