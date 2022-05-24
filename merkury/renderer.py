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
jinja.filters['markdown'] = lambda content: markdown(content, extensions=['tables', ])

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
        if output != '':
            out_chunk += output
            assert(sum([html, markdown]) <= 1, "Only one option can be specified")
            yield {"in": in_chunk, "out": out_chunk, "html": html, "markdown": markdown}
            in_chunk = out_chunk = ""
            html = markdown = False

def produce_report(code, file_name, output_file_path):
    """
    Main function for transforming raw code
    """
    timestamp = datetime.isoformat(datetime.now())
    chunks = tuple(join_chunks(code))
    data = {"chunks": chunks, "timestamp": timestamp, "file_name": file_name}
    template = jinja.get_template("template.html")
    report = template.render(data)
    if output_file_path:
        with open(output_file_path, 'w') as out:
            out.write(report)
    else:
        sys.stdout.write(report)
