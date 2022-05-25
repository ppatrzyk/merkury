"""
Reformats code output into report.
"""

from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown import markdown
import re
import sys

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
            assert(sum([html, markdown]) <= 1, "Only one option can be specified")
            yield {"in": in_chunk, "out": out_chunk, "html": html, "markdown": markdown}
            in_chunk = out_chunk = ""
            html = markdown = False
    if in_chunk != "":
        yield {"in": in_chunk, "out": None, "html": False, "markdown": False}

def produce_report(code, python_file_path, output_file_path):
    """
    Main function for transforming raw code
    """
    timestamp = datetime.now().strftime("%c")
    python_file_name = python_file_path.split("/")[-1]
    chunks = list(join_chunks(code))
    # if last chunk does not print anything, it's appended to previous one
    if (chunks[-1]["out"] is None) and (len(chunks) > 1):
        chunks[-2]["in"] += chunks[-1]["in"]
        del chunks[-1]
    data = {"chunks": chunks, "timestamp": timestamp, "file_name": python_file_name}
    template = jinja.get_template("template.html")
    report = template.render(data)
    if output_file_path:
        with open(output_file_path, "w") as out:
            out.write(report)
    else:
        sys.stdout.write(report)
