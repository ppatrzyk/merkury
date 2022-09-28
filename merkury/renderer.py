"""
Reformats code output into report.
"""

from datetime import datetime
from importlib.metadata import version
from jinja2 import Environment, PackageLoader
from markdown import markdown
from pathlib import Path
import pdfkit
import re

jinja = Environment(
    loader=PackageLoader("merkury", "templates")
)
jinja.filters["markdown"] = lambda content: markdown(content, extensions=["tables", ])

def join_chunks(code):
    """
    Join code nodes without anything printed
    """
    in_chunk = out_chunk = ""
    html = markdown = False
    for input, output in code:
        html = html or any((bool(re.match("^#HTML", line)) for line in input))
        markdown = markdown or any((bool(re.match("^#MARKDOWN", line)) for line in input))
        in_chunk += "".join((line+"\n" for line in input))
        if output != "":
            out_chunk += output
            assert (sum([html, markdown]) <= 1), "Only one option can be specified"
            yield {"in": in_chunk, "out": out_chunk, "html": html, "markdown": markdown}
            in_chunk = out_chunk = ""
            html = markdown = False
    if in_chunk != "":
        yield {"in": in_chunk, "out": None, "html": False, "markdown": False}

def produce_report(code, format, color_theme, python_file_path, output_file_path):
    """
    Main function for transforming raw code
    """
    chunks = list(join_chunks(code))
    # if last chunk does not print anything, it"s appended to previous one
    if (chunks[-1]["out"] is None) and (len(chunks) > 1):
        chunks[-2]["in"] += chunks[-1]["in"]
        del chunks[-1]
    data = {
        "chunks": chunks,
        "color_theme": "light" if (format == "pdf") else color_theme,
        "file_name": python_file_path.name,
        "format": format,
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "version": version("merkury"),
    }
    template = jinja.get_template("template.html")
    report = template.render(data)
    match format:
        case "html":
            with output_file_path.open("w") as out:
                out.write(report)
        case "pdf":
            options = {
                "page-size": "A4",
                "margin-top": "25mm",
                "margin-right": "25mm",
                "margin-bottom": "25mm",
                "margin-left": "25mm",
            }
            pdfkit.from_string(report, output_file_path, options=options)
    return True

def get_default_path(python_file_path, format):
    """
    Default file name for report
    """
    date_now = datetime.now().astimezone().strftime("%Y%m%d%H%M%S%Z")
    file_name = re.sub(".py$", "", python_file_path.name)
    out_file_name = f"{file_name}_{date_now}.{format}"
    return Path(python_file_path.parent, out_file_name)
