import pandas as pd
from bokeh.plotting import figure
from merkury.utils import output_bokeh

iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

intro = """
# Merkury example

This page is an example report generated with [Merkury](https://github.com/ppatrzyk/merkury). It is meant to showcase different formatting possiblities.

This code block is written in markdown. You can use any valid markdown sytax. E.g. for tables:

| Column 1        | Column 2 | Column 3   |
| --------------- | -------- | ---------- |
| _Some value_    | 1        | 3          |
| **Other value** | 2        | 4          |

If you don't specify [formatting options](https://github.com/ppatrzyk/merkury#formatting-and-plots), output will be treated as python code. 

"""

print(intro)
#MARKDOWN

for i in range(10):
    msg = f'Loop iteration: {i}'
    print(msg)

print(iris.head())

html = """
<h3>Custom html header</h3>
<p>This code block is written in raw html.<p>
<img src="data:image/png;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMjggMTI4Ij48bGluZWFyR3JhZGllbnQgaWQ9InB5dGhvbi1vcmlnaW5hbC1hIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjcwLjI1MiIgeTE9IjEyMzcuNDc2IiB4Mj0iMTcwLjY1OSIgeTI9IjExNTEuMDg5IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KC41NjMgMCAwIC0uNTY4IC0yOS4yMTUgNzA3LjgxNykiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzVBOUZENCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzMwNjk5OCIvPjwvbGluZWFyR3JhZGllbnQ+PGxpbmVhckdyYWRpZW50IGlkPSJweXRob24tb3JpZ2luYWwtYiIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiIHgxPSIyMDkuNDc0IiB5MT0iMTA5OC44MTEiIHgyPSIxNzMuNjIiIHkyPSIxMTQ5LjUzNyIgZ3JhZGllbnRUcmFuc2Zvcm09Im1hdHJpeCguNTYzIDAgMCAtLjU2OCAtMjkuMjE1IDcwNy44MTcpIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNGRkQ0M0IiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGRkU4NzMiLz48L2xpbmVhckdyYWRpZW50PjxwYXRoIGZpbGw9InVybCgjcHl0aG9uLW9yaWdpbmFsLWEpIiBkPSJNNjMuMzkxIDEuOTg4Yy00LjIyMi4wMi04LjI1Mi4zNzktMTEuOCAxLjAwNy0xMC40NSAxLjg0Ni0xMi4zNDYgNS43MS0xMi4zNDYgMTIuODM3djkuNDExaDI0LjY5M3YzLjEzN0gyOS45NzdjLTcuMTc2IDAtMTMuNDYgNC4zMTMtMTUuNDI2IDEyLjUyMS0yLjI2OCA5LjQwNS0yLjM2OCAxNS4yNzUgMCAyNS4wOTYgMS43NTUgNy4zMTEgNS45NDcgMTIuNTE5IDEzLjEyNCAxMi41MTloOC40OTFWNjcuMjM0YzAtOC4xNTEgNy4wNTEtMTUuMzQgMTUuNDI2LTE1LjM0aDI0LjY2NWM2Ljg2NiAwIDEyLjM0Ni01LjY1NCAxMi4zNDYtMTIuNTQ4VjE1LjgzM2MwLTYuNjkzLTUuNjQ2LTExLjcyLTEyLjM0Ni0xMi44MzctNC4yNDQtLjcwNi04LjY0NS0xLjAyNy0xMi44NjYtMS4wMDh6TTUwLjAzNyA5LjU1N2MyLjU1IDAgNC42MzQgMi4xMTcgNC42MzQgNC43MjEgMCAyLjU5My0yLjA4MyA0LjY5LTQuNjM0IDQuNjktMi41NiAwLTQuNjMzLTIuMDk3LTQuNjMzLTQuNjktLjAwMS0yLjYwNCAyLjA3My00LjcyMSA0LjYzMy00LjcyMXoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTAuMjYpIi8+PHBhdGggZmlsbD0idXJsKCNweXRob24tb3JpZ2luYWwtYikiIGQ9Ik05MS42ODIgMjguMzh2MTAuOTY2YzAgOC41LTcuMjA4IDE1LjY1NS0xNS40MjYgMTUuNjU1SDUxLjU5MWMtNi43NTYgMC0xMi4zNDYgNS43ODMtMTIuMzQ2IDEyLjU0OXYyMy41MTVjMCA2LjY5MSA1LjgxOCAxMC42MjggMTIuMzQ2IDEyLjU0NyA3LjgxNiAyLjI5NyAxNS4zMTIgMi43MTMgMjQuNjY1IDAgNi4yMTYtMS44MDEgMTIuMzQ2LTUuNDIzIDEyLjM0Ni0xMi41NDd2LTkuNDEySDYzLjkzOHYtMy4xMzhoMzcuMDEyYzcuMTc2IDAgOS44NTItNS4wMDUgMTIuMzQ4LTEyLjUxOSAyLjU3OC03LjczNSAyLjQ2Ny0xNS4xNzQgMC0yNS4wOTYtMS43NzQtNy4xNDUtNS4xNjEtMTIuNTIxLTEyLjM0OC0xMi41MjFoLTkuMjY4ek03Ny44MDkgODcuOTI3YzIuNTYxIDAgNC42MzQgMi4wOTcgNC42MzQgNC42OTIgMCAyLjYwMi0yLjA3NCA0LjcxOS00LjYzNCA0LjcxOS0yLjU1IDAtNC42MzMtMi4xMTctNC42MzMtNC43MTkgMC0yLjU5NSAyLjA4My00LjY5MiA0LjYzMy00LjY5MnoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDAgMTAuMjYpIi8+PHJhZGlhbEdyYWRpZW50IGlkPSJweXRob24tb3JpZ2luYWwtYyIgY3g9IjE4MjUuNjc4IiBjeT0iNDQ0LjQ1IiByPSIyNi43NDMiIGdyYWRpZW50VHJhbnNmb3JtPSJtYXRyaXgoMCAtLjI0IC0xLjA1NSAwIDUzMi45NzkgNTU3LjU3NikiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNCOEI4QjgiIHN0b3Atb3BhY2l0eT0iLjQ5OCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzdGN0Y3RiIgc3RvcC1vcGFjaXR5PSIwIi8+PC9yYWRpYWxHcmFkaWVudD48cGF0aCBvcGFjaXR5PSIuNDQ0IiBmaWxsPSJ1cmwoI3B5dGhvbi1vcmlnaW5hbC1jKSIgZD0iTTk3LjMwOSAxMTkuNTk3YzAgMy41NDMtMTQuODE2IDYuNDE2LTMzLjA5MSA2LjQxNi0xOC4yNzYgMC0zMy4wOTItMi44NzMtMzMuMDkyLTYuNDE2IDAtMy41NDQgMTQuODE1LTYuNDE3IDMzLjA5Mi02LjQxNyAxOC4yNzUgMCAzMy4wOTEgMi44NzIgMzMuMDkxIDYuNDE3eiIvPjwvc3ZnPgo=" />
<p>
In addition to writing content manually, any python package that produces custom HTML output can be used here. 
See printing pandas dataframes and plotting with bokeh below.
</p>
"""

print(html)
#HTML

iris_html = iris.head(10).to_html(border=0)
print(f"<h3>Iris dataset</h3>{iris_html}")
#HTML

colors = pd.DataFrame({"species": ["setosa", "virginica", "versicolor", ], "color": ["blue", "green", "red"]})
iris = iris.merge(colors, how="left")

plot = figure(
    title="Iris species",
    x_axis_label="petal_width",
    y_axis_label="sepal_width"
)
plot.circle(
    iris["petal_width"],
    iris["sepal_width"],
    fill_color = iris["color"],
    size = 10
)

print(output_bokeh(plot))
#HTML
