"""
Module for running the script.

Code is adapted from the following SO question
https://stackoverflow.com/questions/60297105/python-write-both-commands-and-their-output-to-a-file
"""

import ast
import sys

def execute(path):
    """
    Run python script
    """
    with open(path, 'r') as file:
        lines = file.readlines()
    print(lines)

