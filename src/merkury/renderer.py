"""
Reformats code out_code into report.
"""

from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown import markdown
from pathlib import Path
import logging
import re
from .runner_py import Code
from .utils import VERSION

jinja = Environment(
    loader=PackageLoader(__package__, "templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)
jinja.filters["markdown"] = lambda content: markdown(content, extensions=["tables", ])

def _generate_chunks_internal(code: Code):
    """
    Join code nodes
    """
    in_chunk = out_chunk = ""
    html = markdown = False
    title = None
    for in_code, out_code in code:
        html = html or any((bool(re.match(r"^#HTML", line)) for line in in_code))
        markdown = markdown or any((bool(re.match(r"^#MARKDOWN", line)) for line in in_code))
        for line in in_code:
            if re.search(r"^#TITLE", line):
                title = re.sub(r"^#TITLE\s+", "", line)
        in_chunk += "".join((line+"\n" for line in in_code))
        if out_code != "":
            out_chunk += out_code
            assert (sum([html, markdown]) <= 1), "Both html and markdown specified for a chunk"
            yield {"in": in_chunk, "out": out_chunk, "html": html, "markdown": markdown, "title": title}
            in_chunk = out_chunk = ""
            html = markdown = False
            title = None
    if in_chunk != "":
        yield {"in": in_chunk, "out": None, "html": False, "markdown": False, "title": title}

def generate_chunks(code: Code):
    """
    Turn raw code into chunks used for report
    """
    chunks = [{"number": i, **chunk} for i, chunk in enumerate(_generate_chunks_internal(code), start=1)]
    # if last chunk does not print anything, it"s appended to previous one
    if (len(chunks) > 1) and (chunks[-1]["out"] is None):
        chunks[-2]["in"] += chunks[-1]["in"]
        del chunks[-1]
    return chunks

def generate_report(code: Code, report_file_path: Path, template_data: dict) -> bool:
    """
    Main function for transforming raw code
    """
    chunks = generate_chunks(code)
    output_format = template_data.get("output_format")
    template = jinja.get_template(f"template.{output_format}.jinja")
    report = template.render({
        **template_data,
        "chunks": chunks,
        "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "version": VERSION,
    })
    with report_file_path.open("w") as out:
        out.write(report)
    logging.debug(f"Report written to {report_file_path}")
    return True
