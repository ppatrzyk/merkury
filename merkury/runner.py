"""
Module for running the script.

Code is adapted from the following SO question
https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file
"""

import ast
from contextlib import redirect_stdout
from io import StringIO
from itertools import starmap

ENV = {'__name__': '__main__'}

def get_node_end(node):
    """
    Helper for finding last line for ast node
    """
    max_line_no = getattr(node, "max_lineno") if hasattr(node, "max_lineno") else 0
    line_no = getattr(node, "lineno") if hasattr(node, "lineno") else 0
    return max(max_line_no, line_no)

def get_code_out(node, file_name):
    """
    Get code output from given node
    """
    f = StringIO()
    with redirect_stdout(f):
        print(node)
        exec(compile(ast.Module([node, ], type_ignores=[]), file_name, 'exec'), ENV)
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
    
    end_lines = tuple(map(get_node_end, module.body))
    start_lines = (0, ) + tuple(el-1 for el in end_lines[:-1])
    indices = zip(start_lines, end_lines)
    print(tuple(indices))
    code_outputs = tuple(starmap(get_code_out, ((node, file_name, ) for node in module.body)))
    print(code_outputs)
    