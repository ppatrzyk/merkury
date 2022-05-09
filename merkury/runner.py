"""
Module for running the script.

Code is adapted from the following SO question
https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file
"""

import ast
import sys

ENV = {'__name__': '__main__'}

def get_node_end(node):
    """
    Helper for finding last line for ast node
    """
    max_line_no = getattr(node, "max_lineno") if hasattr(node, "max_lineno") else 0
    line_no = getattr(node, "lineno") if hasattr(node, "lineno") else 0
    return max(max_line_no, line_no)

def execute(path):
    """
    Run python script
    """
    file_name = path.split("/")[-1]
    with open(path, 'r') as file:
        source = file.read()
    lines = source.split("\n")
    module = ast.parse(source, file_name)
    
    start_line = 0
    end_line = None
    for node in module.body:
        end_line = get_node_end(node)
        print(node)
        print(end_line)
