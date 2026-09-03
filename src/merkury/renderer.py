"""
Reformats code out_code into report.
"""

import re
from collections.abc import Iterator
from datetime import datetime

from jinja2 import Environment, PackageLoader
from markdown import markdown

from .utils import VERSION

Code = Iterator[tuple[list[str], str, float]]

jinja = Environment(
    loader=PackageLoader(__package__, "templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)
jinja.filters["markdown"] = lambda content: markdown(
    content,
    extensions=[
        "fenced_code",
        "tables",
        "toc",
    ],
)


def _generate_chunks_internal(code: Code):
    """
    Join code nodes
    """
    in_chunk = out_chunk = ""
    html = markdown = False
    title = None
    chunk_duration_ms = 0
    for in_code, out_code, duration_ms in code:
        html = html or any(bool(re.match(r"^#HTML", line)) for line in in_code)
        markdown = markdown or any(
            bool(re.match(r"^#MARKDOWN", line)) for line in in_code
        )
        for line in in_code:
            if re.search(r"^#TITLE", line):
                title = re.sub(r"^#TITLE\s+", "", line)
        in_chunk += "".join(line + "\n" for line in in_code)
        chunk_duration_ms += duration_ms
        if out_code != "":
            out_chunk += out_code
            assert sum([html, markdown]) <= 1, (
                "Both html and markdown specified for a chunk"
            )
            yield {
                "in": in_chunk,
                "out": out_chunk,
                "html": html,
                "markdown": markdown,
                "title": title,
                "chunk_duration_ms": round(chunk_duration_ms),
            }
            in_chunk = out_chunk = ""
            html = markdown = False
            title = None
            chunk_duration_ms = 0
    if in_chunk != "":
        yield {
            "in": in_chunk,
            "out": None,
            "html": False,
            "markdown": False,
            "title": title,
            "chunk_duration_ms": round(chunk_duration_ms),
        }


def generate_chunks(code: Code) -> list[dict]:
    """
    Turn raw code into chunks used for report
    """
    chunks = []
    for i, chunk in enumerate(_generate_chunks_internal(code), start=1):
        chunk["number"] = i
        if chunk.get("title") is None:
            chunk["title"] = f"Chunk {i}"
        chunk["node_id"] = chunk["title"].lower().replace(" ", "-")
        chunks.append(chunk)
    # if last chunk does not print anything, it is appended to previous one
    if (len(chunks) > 1) and (chunks[-1]["out"] is None):
        chunks[-2]["in"] += chunks[-1]["in"]
        chunks[-2]["chunk_duration_ms"] += chunks[-1]["chunk_duration_ms"]
        del chunks[-1]
    return chunks


def generate_report(code: Code, template_data: dict) -> str:
    """
    Main function for transforming raw code
    """
    chunks = generate_chunks(code)
    output_format = template_data.get("output_format")
    template = jinja.get_template(f"template.{output_format}.jinja")
    report = template.render(
        {
            **template_data,
            "chunks": chunks,
            "timestamp": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
            "version": VERSION,
        }
    )
    return report
