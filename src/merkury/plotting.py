"""
Plotting utility functions
"""

import base64
import io
import json
import os
import tempfile
import uuid

DEFAULT_HEIGHT = 800
DEFAULT_WIDTH = 800


def _print_plot_container(html: str):
    """
    Wrapper for centering
    """
    wrapped_html = f"""
    <div class="merkury-plot-container">
    {html}
    </div>
    """
    print(wrapped_html)


def _bytes_to_html(bytes):
    """
    Helper for getting base64 encoded img html tag
    """
    img_encoded = base64.b64encode(bytes).decode()
    img_html = f"""
    <img src="data:image/png;base64,{img_encoded}" />
    """
    return _print_plot_container(img_html)


def _create_iframe(
    plot_html: str,
    height: int | None = DEFAULT_HEIGHT,
    width: int | None = DEFAULT_WIDTH,
):
    """
    Iframe wrapper for plots exported as full html page
    """
    id_suffix = uuid.uuid4().hex
    plot_html_encoded = json.dumps(base64.b64encode(plot_html.encode()).decode())
    if height is None:
        height = DEFAULT_HEIGHT
    if width is None:
        width = DEFAULT_WIDTH
    html_part = f"""
    <iframe id="iframe-{id_suffix}" class="merkury-plot-iframe" style="height: {height}px; width: {width}px"></iframe>
    <script>
    const iframe_{id_suffix} = document.getElementById('iframe-{id_suffix}');
    const srcdoc_{id_suffix} = atob({plot_html_encoded});
    iframe_{id_suffix}.srcdoc = srcdoc_{id_suffix};
    </script>
    """
    return _print_plot_container(html_part)


def output_altair(figure):
    """
    Process altair figure
    """
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    figure.save(temp.name)
    with open(temp.name, "r") as f:
        rendered_figure = f.read()
    os.remove(temp.name)
    fig_dict = figure.to_dict()
    width = height = None
    width_raw = fig_dict.get("config", {}).get("view", {}).get("continuousWidth")
    if width_raw is not None:
        width = width_raw + 100
    height_raw = fig_dict.get("config", {}).get("view", {}).get("continuousHeight")
    if height_raw is not None:
        height = height_raw + 100

    return _create_iframe(
        rendered_figure,
        width=width,
        height=height,
    )


def output_bokeh(figure):
    """
    Process boheh figure
    """
    from bokeh.embed import file_html
    from bokeh.resources import CDN

    return _create_iframe(
        file_html(figure, CDN, "Bokeh plot"), width=figure.width, height=figure.height
    )


def output_matplotlib(figure):
    """
    Process matplotlib figure
    """
    fig_bytes = io.BytesIO()
    figure.savefig(fig_bytes, format="png")
    fig_bytes.seek(0)
    return _bytes_to_html(fig_bytes.read())


def output_plotly(figure):
    """
    Process plotly figure
    """
    import plotly

    return _create_iframe(
        plotly.io.to_html(figure, include_plotlyjs="cdn"),
        width=figure.layout.width,
        height=figure.layout.height,
    )


def output_pyecharts(figure):
    """
    Process pyecharts figure
    """
    return _create_iframe(
        figure.render_embed(),
        width=int(figure.width.strip("px")),
        height=int(figure.height.strip("px")),
    )
