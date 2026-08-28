"""
Functions for running python scripts.
"""

import ast
import logging
import traceback
from contextlib import redirect_stdout
from io import StringIO
from itertools import starmap
from pathlib import Path
from typing import Iterator

Code = Iterator[tuple[list[str], str]]

ENV = {"__name__": "__main__"}

def get_node_line(node: ast.stmt):
    """
    Helper for finding starting line for ast node
    Line numbers are 1-indexed, hence conversion
    """
    return (getattr(node, "lineno") - 1)

def get_code_out(node: ast.stmt, file_name: str) -> tuple[bool, str]:
    """
    Get code output from given node
    """
    f = StringIO()
    code = compile(ast.Module([node, ], type_ignores=[]), file_name, "exec")
    success = False
    with redirect_stdout(f):
        try:
            exec(code, ENV)
            success = True
        except Exception as e:
            msg = f"{type(e).__name__}: {e}"
            print(msg)
    return success, f.getvalue()

def prune_lines(lines: list[str]) -> list[str]:
    """
    Prune empty lines at the end from code chunk
    """
    if (not lines) or (lines[-1] != ""):
        return lines
    else:
        return prune_lines(lines[:-1])

def execute_python(script_path: Path) -> Code:
    """
    Run python script
    """
    with script_path.open("r") as file:
        source = file.read()
    lines = source.split("\n")
    module: ast.Module = ast.parse(source, script_path.name)
    start_lines = tuple(map(get_node_line, module.body))
    end_lines = start_lines[1:] + (len(lines), )
    code_inputs = tuple(prune_lines(lines[start:end]) for start, end in zip(start_lines, end_lines))
    code_inputs_len = len(code_inputs)
    assert code_inputs_len > 0, "Python file is empty"
    code_outputs = list()
    for i, node in enumerate(module.body, start=1):
        logging.debug(f"Running [{i}/{code_inputs_len}]")
        success, output = get_code_out(node, script_path.name)
        code_outputs.append(output)
        if not success:
            logging.warning("Code raised exception, execution stopped")
            break
    return zip(code_inputs, code_outputs)
