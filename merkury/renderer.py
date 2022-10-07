"""
Reformats code output into report.
"""

from jinja2 import Environment, PackageLoader
from markdown import markdown
import pdfkit
import re

jinja = Environment(
    loader=PackageLoader("merkury", "templates")
)
jinja.filters["markdown"] = lambda content: markdown(content, extensions=["tables", ])

PDFKIT_OPTS = {
    "page-size": "A4",
    "margin-top": "25mm",
    "margin-right": "25mm",
    "margin-bottom": "25mm",
    "margin-left": "25mm",
}

def chunk_generator(code, script_type):
    """
    Join code nodes
    """
    in_chunk = out_chunk = ""
    html = markdown = False
    for input, output in code:
        if script_type == ".py":
            html = html or any((bool(re.match("^#HTML", line)) for line in input))
            markdown = markdown or any((bool(re.match("^#MARKDOWN", line)) for line in input))
        elif script_type == ".sql":
            html = True
            markdown = False
        in_chunk += "".join((line+"\n" for line in input))
        if output != "":
            out_chunk += output
            assert (sum([html, markdown]) <= 1), "Only one option can be specified"
            yield {"in": in_chunk, "out": out_chunk, "html": html, "markdown": markdown}
            in_chunk = out_chunk = ""
            html = markdown = False
    if in_chunk != "":
        yield {"in": in_chunk, "out": None, "html": False, "markdown": False}

def join_chunks(code, script_type):
    """
    Turn raw code into chunks used for report
    """
    chunks = list(chunk_generator(code, script_type))
    # if last chunk does not print anything, it"s appended to previous one
    if (len(chunks) > 1) and (chunks[-1]["out"] is None):
        chunks[-2]["in"] += chunks[-1]["in"]
        del chunks[-1]
    return chunks

def produce_report(code, report_file_path, template_data):
    """
    Main function for transforming raw code
    """
    chunks = join_chunks(code, template_data.get("script_type"))
    data = {**template_data, "chunks": chunks,}
    template = jinja.get_template("template.html")
    report = template.render(data)
    match data.get("format"):
        case "html":
            with report_file_path.open("w") as out:
                out.write(report)
        case "pdf":
            pdfkit.from_string(report, report_file_path, options=PDFKIT_OPTS)
    return True
