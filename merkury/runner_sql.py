"""
Functions for runnig SQL scripts
"""
from itertools import starmap
import prettytable
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

def trigger_query(cursor, query):
    """
    Run query and return result
    """
    result = cursor.execute(query)
    table = prettytable.from_db_cursor(result)
    table = "" if table is None else table.get_string()
    return table

def execute_sqlite(db_path, script_path):
    """
    Run sql script on SQLite DB
    """
    code_inputs = generate_satements(script_path)
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    code_outputs = tuple(starmap(trigger_query, ((cur, "\n".join(query), ) for query in code_inputs)))
    return zip(code_inputs, code_outputs)
