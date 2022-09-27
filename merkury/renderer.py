"""
Reformats code output into report.
"""

from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown import markdown
from pathlib import Path
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

def produce_report(code, format, python_file_name, output_file_path):
    """
    Main function for transforming raw code
    """
    timestamp = datetime.now().strftime("%c")
    chunks = list(join_chunks(code))
    # if last chunk does not print anything, it's appended to previous one
    if (chunks[-1]["out"] is None) and (len(chunks) > 1):
        chunks[-2]["in"] += chunks[-1]["in"]
        del chunks[-1]
    data = {"chunks": chunks, "timestamp": timestamp, "file_name": python_file_name}
    template = jinja.get_template("template.html")
    report = template.render(data)
    with output_file_path.open("w") as out:
        out.write(report)
    return True

def get_default_path(python_file_path, format):
    """
    Default file name for report
    """
    date_now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    file_name = re.sub(".py$", "", python_file_path.name)
    out_file_name = f'{file_name}_{date_now}.{format}'
    return Path(python_file_path.parent, out_file_name)
