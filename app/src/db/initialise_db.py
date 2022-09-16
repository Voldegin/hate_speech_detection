# Public Imports
import sqlite3
from sqlalchemy import create_engine
import os


def initialize_db():
    connection = sqlite3.connect('database.db')

    schema_file = os.path.join(os.getcwd(), "src//db//schema.sql")

    with open(schema_file) as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()

    db_path = os.path.join(os.getcwd(), "database.db")

    engine = create_engine('sqlite:///' + db_path, echo=False)
    return engine
