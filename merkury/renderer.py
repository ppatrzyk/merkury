"""
Reformats code output into report.
"""

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

def produce_report(code_inputs, code_outputs):
    """
    Main function for transforming raw code
    """
    print(code_inputs)
    print(code_outputs)
    chunks = tuple(join_chunks(code_inputs, code_outputs))
    print(chunks)
