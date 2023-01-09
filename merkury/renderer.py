"""
Reformats code output into report.
"""

from jinja2 import Environment, PackageLoader
from markdown import markdown
import re

jinja = Environment(
    loader=PackageLoader("merkury", "templates")
)
jinja.filters["markdown"] = lambda content: markdown(content, extensions=["tables", ])

COMMENT = {"python": "#", "SQL": "--"}

def chunk_generator(code, script_type):
    """
    Join code nodes
    """
    in_chunk = out_chunk = ""
    html = markdown = False
    titles = [None, ]
    for input, output in code:
        if script_type == "python":
            html = html or any((bool(re.match("^#HTML", line)) for line in input))
            markdown = markdown or any((bool(re.match("^#MARKDOWN", line)) for line in input))
        elif script_type == "SQL":
            html = True
            markdown = False
        titles.extend(re.sub(f"^{COMMENT[script_type]}TITLE\s+", "", line) for line in input if re.search(f"^{COMMENT[script_type]}TITLE", line))
        in_chunk += "".join((line+"\n" for line in input))
        if output != "":
            out_chunk += output
            assert (sum([html, markdown]) <= 1), "Both html and markdown specified for a chunk"
            yield {"in": in_chunk, "out": out_chunk, "html": html, "markdown": markdown, "title": titles[-1]}
            in_chunk = out_chunk = ""
            html = markdown = False
            titles = [None, ]
    if in_chunk != "":
        yield {"in": in_chunk, "out": None, "html": False, "markdown": False, "title": titles[-1]}

def join_chunks(code, script_type):
    """
    Turn raw code into chunks used for report
    """
    chunks = [{"number": el[0], **el[1]} for el in enumerate(chunk_generator(code, script_type), start=1)]
    # if last chunk does not print anything, it"s appended to previous one
    if (len(chunks) > 1) and (chunks[-1]["out"] is None):
        chunks[-2]["in"] += chunks[-1]["in"]
        del chunks[-1]
    return chunks

def produce_report(template_data):
    """
    Main function for transforming raw code
    """
    template = jinja.get_template(f"template.{template_data.get('format')}")
    chunks = join_chunks(template_data.get("code"), template_data.get("script_type"))
    report = template.render({**template_data, "chunks": chunks, })
    with template_data.get("report_file_path").open("w") as out:
        out.write(report)
    return True
