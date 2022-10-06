"""
Functions for runnig SQL scripts
"""
import sqlite3
import sqlparse

def generate_satements(script_path):
    """
    Generate SQL statements form raw file lines
    """
    with script_path.open("r") as file:
        source = file.read()
    statements = [el.split("\n") for el in sqlparse.split(source)]
    return statements

def execute_sqlite(db_path, script_path):
    """
    Run sql script on SQLite DB
    """
    con = sqlite3.connect(db_path)
    code_inputs = generate_satements(script_path)
    print(code_inputs)
    # TODO cursor and execute statements, prettytable formatting
    raise NotImplementedError("TODO")
