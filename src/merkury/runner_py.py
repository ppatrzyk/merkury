"""
Functions for running python scripts.
"""

import ast
import logging
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from time import time

from .renderer import Code, generate_report

ENV = {"__name__": "__main__"}

logger = logging.getLogger(__name__)


def _get_node_line(node: ast.stmt):
    """
    Helper for finding starting line for ast node
    Line numbers are 1-indexed, hence conversion
    """
    return node.lineno - 1


def _get_code_output(node: ast.stmt, file_name: str) -> tuple[bool, str]:
    """
    Get code output from given node
    """
    f = StringIO()
    code = compile(
        ast.Module(
            [
                node,
            ],
            type_ignores=[],
        ),
        file_name,
        "exec",
    )
    success = False
    with redirect_stdout(f):
        try:
            exec(code, ENV)  # noqa
            success = True
        except Exception as e:  # noqa
            msg = f"{type(e).__name__}: {e}"
            print(msg)
    return success, f.getvalue()


def _prune_lines(lines: list[str]) -> list[str]:
    """
    Prune empty lines at the end from code chunk
    """
    if (not lines) or (lines[-1] != ""):
        return lines
    else:
        return _prune_lines(lines[:-1])


def _execute_python(script_path: Path) -> tuple[float, Code]:
    """
    Run python script
    """
    start = time()
    with script_path.open("r") as file:
        source = file.read()
    lines = source.split("\n")
    module: ast.Module = ast.parse(source, script_path.name)
    start_lines = tuple(map(_get_node_line, module.body))
    end_lines = start_lines[1:] + (len(lines),)
    code_inputs = tuple(
        _prune_lines(lines[start:end]) for start, end in zip(start_lines, end_lines)
    )
    code_inputs_len = len(code_inputs)
    assert code_inputs_len > 0, "Python file is empty"
    code_outputs = []
    for i, node in enumerate(module.body, start=1):
        logger.debug(f"Running [{i}/{code_inputs_len}]")
        success, output = _get_code_output(node, script_path.name)
        code_outputs.append(output)
        if not success:
            logger.warning("Code raised exception, execution stopped")
            break
    duration_ms = int(1000 * (time() - start))
    return duration_ms, zip(code_inputs, code_outputs)


def get_report(path: Path, report_file_path: Path, template_data: dict) -> bool:
    if template_data.get("title") is None:
        template_data = {**template_data, "title": path.name}
    duration_ms, code = _execute_python(path)
    template_data = {
        **template_data,
        "duration_ms": duration_ms,
        "file_name": path.name,
    }
    report = generate_report(code, template_data)
    with report_file_path.open("w") as out:
        out.write(report)
    logger.debug(f"Report written to {report_file_path}")
    return True
