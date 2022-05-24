from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

intro = """
# Bokeh usage

Example of how to include bokeh plots in merkury HTML reports.
"""
print(intro)
#MARKDOWN

plot = figure()
plot.circle([1, 2, 3, ], [3, 5, 4, ])

html = file_html(plot, CDN, "Bokeh plot")
print(html)
#HTML