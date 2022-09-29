import os
import tempfile
import altair as alt
from merkury.utils import output_altair

intro = """
# Altair usage

Example of how to include altair (vega) plots in merkury HTML reports.
"""
print(intro)
#MARKDOWN

data = alt.Data(values=[{"x": 5, "y": 6}, {"x": 6, "y": 7}, {"x": 7, "y": 4}])
chart = alt.Chart(data).mark_point().encode(
    x="x:Q",
    y="y:Q",
)

print(output_altair(chart))
#HTML
