"""
Functions for runnig SQL scripts
"""
from itertools import starmap
import prettytable
import psycopg
import re
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
    table = "" if table is None else table.get_html_string()
    return table

def execute_sql(db_path, script_path):
    """
    Run sql script on SQL DB
    Supported: SQLite, PostgreSQL
    """
    code_inputs = generate_satements(script_path)
    if re.search(r"(^postgres://|^postgresql://)", db_path):
        db_conn = psycopg.connect(db_path)
    else:
        # ":memory:" or file path
        db_conn = sqlite3.connect(db_path)
        db_conn.row_factory = sqlite3.Row
    cur = db_conn.cursor()
    code_outputs = tuple(starmap(trigger_query, ((cur, "\n".join(query), ) for query in code_inputs)))
    db_conn.close()
    return zip(code_inputs, code_outputs)
