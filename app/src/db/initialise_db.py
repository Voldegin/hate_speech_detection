# Public Imports
import sqlite3
import os


def initialize_db():
    connection = sqlite3.connect('database.db')

    schema_file = os.path.join(os.getcwd(), "src//db//schema.sql")

    with open(schema_file) as f:
        connection.executescript(f.read())

    connection.commit()
    return connection
