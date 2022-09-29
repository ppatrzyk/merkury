from bokeh.plotting import figure
from merkury.utils import output_bokeh

intro = """
# Bokeh usage

Example of how to include bokeh plots in merkury HTML reports.
"""
print(intro)
#MARKDOWN

plot = figure()
plot.circle([1, 2, 3, ], [3, 5, 4, ])

print(output_bokeh(plot))
#HTML