"""
Utility functions for code output formatting
"""

import base64
import io
import os
import tempfile

# TODO making altair and bokeh charts non-interactive (png)
# for pdfs possible, but would require js dependencies see
# https://pypi.org/project/altair-saver/
# https://docs.bokeh.org/en/latest/docs/user_guide/export.html#additional-dependencies

def output_altair(figure):
    """
    Process altair figure
    """
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    figure.save(temp.name)
    with open(temp.name, "r") as f:
        rendered_figure = f.read()
    os.remove(temp.name)
    return rendered_figure

def output_bokeh(figure):
    """
    Process boheh figure
    """
    from bokeh.embed import file_html
    from bokeh.resources import CDN
    return file_html(figure, CDN, "Bokeh plot")

def output_matplotlib(figure):
    """
    Process matplotlib figure
    """
    fig_bytes = io.BytesIO()
    figure.savefig(fig_bytes, format="png")
    fig_bytes.seek(0)
    return _bytes_to_html(fig_bytes.read())

def output_plotly(figure, interactive=True):
    """
    Process plotly figure
    """
    import plotly
    if interactive:
        return plotly.io.to_html(figure, include_plotlyjs="cdn")
    else:
        img_bytes = figure.to_image(format="png")
        return _bytes_to_html(img_bytes)

def _bytes_to_html(bytes):
    """
    Helper for getting base64 encoded img html tag
    """
    img_encoded = base64.b64encode(bytes).decode()
    img_html = f"""<img src="data:image/png;base64,{img_encoded}" />"""
    return img_html
