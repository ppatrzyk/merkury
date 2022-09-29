import pandas as pd
from bokeh.plotting import figure
from merkury.utils import output_bokeh

iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

intro = """
# Merkury example

This page is an example report generated with [Merkury](https://github.com/ppatrzyk/merkury). It is meant to showcase different formatting possiblities.

This code block is written in markdown. You can use any valid markdown sytax. E.g. for tables:

| Column 1    | Column 2 | Column 3   |
| ----------- | -------- | ---------- |
| Some value  | _1_      | _3_        |
| Other value | **2**    | **4**      |

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
<img src="https://www.python.org/static/img/python-logo-large.c36dccadd999.png" alt="python">
<p>
In addition to writing content manually, any python package that produces custom HTML output can be used here. 
See printing dataframes with pandas and plotting with bokeh below.
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
