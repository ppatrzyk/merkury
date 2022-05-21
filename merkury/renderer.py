"""
Reformats code output into report.
"""

import re
from jinja2 import Environment, FileSystemLoader

jinja = Environment(
    loader=FileSystemLoader("merkury/templates")
)

def join_chunks(code_inputs, code_outputs):
    """
    Join code nodes without anything printed
    """
    in_chunk = out_chunk = ""
    raw_html = False
    for input, output in zip(code_inputs, code_outputs):
        raw_html = raw_html or any((bool(re.match("^#RAW", line)) for line in input))
        in_chunk += "".join((line+"\n" for line in input))
        if output != '':
            out_chunk += output
            yield {"in": in_chunk, "out": out_chunk, "raw_html": raw_html}
            in_chunk = out_chunk = ""
            raw_html = False

def generate_template(chunks):
    """
    Put code chunks into proper template
    """
    template = jinja.get_template("template.html")
    print(template.render({"chunks": chunks}))

def produce_report(code_inputs, code_outputs):
    """
    Main function for transforming raw code
    """
    chunks = tuple(join_chunks(code_inputs, code_outputs))
    generate_template(chunks)
