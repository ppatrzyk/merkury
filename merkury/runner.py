"""
Functions for running the script.
"""

import ast
from contextlib import redirect_stdout
from io import StringIO
from itertools import starmap
import sqlite3

ENV = {"__name__": "__main__"}

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
    code = compile(ast.Module([node, ], type_ignores=[]), file_name, "exec")
    with redirect_stdout(f):
        exec(code, ENV)
    return f.getvalue()

def execute_python(script_path):
    """
    Run python script
    """
    with script_path.open("r") as file:
        source = file.read()
    lines = source.split("\n")
    module = ast.parse(source, script_path.name)
    start_lines = tuple(map(get_node_line, module.body))
    end_lines = start_lines[1:] + (len(lines), )
    code_inputs = tuple(lines[start:end] for start, end in zip(start_lines, end_lines))
    assert code_inputs, "Python file is empty"
    code_outputs = tuple(starmap(get_code_out, ((node, script_path.name, ) for node in module.body)))
    return zip(code_inputs, code_outputs)

def execute_sqlite(db_path, script_path):
    """
    Run sql script on SQLite DB
    """
    con = sqlite3.connect(db_path)
    with script_path.open("r") as file:
        source = file.read()
    # TODO by line OR split on statements (;)
    lines = source.split("\n")
    print(lines)
    statements = source.split(";")
    # TODO keep ; at the end of line
    print(statements)
    # TODO how formatting comments #HTML are read here (before/after)
    # TODO cursor and execute statements, prettytable formatting
    raise NotImplementedError("TODO")
