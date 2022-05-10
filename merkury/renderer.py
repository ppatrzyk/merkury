"""
Reformats code output into report.
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja = Environment(
    loader=FileSystemLoader("merkury/templates"),
    autoescape=select_autoescape()
)

def join_chunks(code_inputs, code_outputs):
    """
    Join code nodes without anything printed
    """
    in_chunk = out_chunk = ""
    for input, output in zip(code_inputs, code_outputs):
        in_chunk += "".join((line+"\n" for line in input))
        match output:
            case '':
                pass
            case _:
                out_chunk += output
                yield {"in": in_chunk, "out": out_chunk}
                in_chunk = out_chunk = ""

def generate_template(chunks):
    """
    Put code chunks into proper template
    """
    template = jinja.get_template("template.html")
    print(template.render({"content": "here"}))
    print(chunks)

def produce_report(code_inputs, code_outputs):
    """
    Main function for transforming raw code
    """
    chunks = tuple(join_chunks(code_inputs, code_outputs))
    generate_template(chunks)
