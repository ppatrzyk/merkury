"""
Functions for running the script.
"""

import ast
from contextlib import redirect_stdout
from io import StringIO
from itertools import starmap

ENV = {'__name__': '__main__'}

def get_node_line(node):
    """
    Helper for finding starting line for ast node
    Line numbers are 1-indexed, hence conversion
    """
    return (getattr(node, "lineno") - 1)

def get_code_out(node, file_name):
    """
    Get code output from given node
    """
    f = StringIO()
    code = compile(ast.Module([node, ], type_ignores=[]), file_name, 'exec')
    with redirect_stdout(f):
        exec(code, ENV)
    return f.getvalue()

def execute(path):
    """
    Run python script
    """
    file_name = path.split("/")[-1]
    with open(path, 'r') as file:
        source = file.read()
    lines = source.split("\n")
    module = ast.parse(source, file_name)
    start_lines = tuple(map(get_node_line, module.body))
    end_lines = start_lines[1:] + (len(lines), )
    code_inputs = tuple(lines[start:end] for start, end in zip(start_lines, end_lines))
    code_outputs = tuple(starmap(get_code_out, ((node, file_name, ) for node in module.body)))
    return zip(code_inputs, code_outputs)
