"""
Utility functions for code output formatting
"""

import altair as alt
import bokeh
import matplotlib
import plotly

# TODO fix imports such that matching works
# test on different plot classes (possible?)

def fig_out(content, interactive=True):
    """
    Helper function to turn figure into html
    """
    match content:
        case alt.Chart():
            return _process_altair(content, interactive)
        case bokeh.plotting.Figure():
            return _process_bokeh(content, interactive)
        case matplotlib.figure.Figure():
            return _process_matplotlib(content, interactive)
        case plotly.graph_objs._figure.Figure():
            return _process_plotly(content, interactive)
        case _:
            raise ValueError(f"Cannot process type {str(type(content))}")

def _process_altair(content, interactive):
    """
    Process altair figure
    """
    print("Altair detected")
    return True

def _process_bokeh(content, interactive):
    """
    Process boheh figure
    """
    print("Bokeh detected")
    return True

def _process_matplotlib(content, interactive):
    """
    Process matplotlib figure
    """
    print("Matplotlib detected")
    return True

def _process_plotly(content, interactive):
    """
    Process plotly figure
    """
    print("Plotly detected")
    return True
