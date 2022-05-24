import os
import tempfile
import altair as alt

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

temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
chart.save(temp.name)

with open(temp.name, "r") as f:
    rendered_chart = f.read()
    print(rendered_chart)
#HTML

os.remove(temp.name)
