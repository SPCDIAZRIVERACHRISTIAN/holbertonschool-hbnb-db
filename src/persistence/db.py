"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""

from src.models.base import Base
from src.persistence.repository import Repository
import os
import sqlite3


class DBRepository(Repository):
    def __init__(self) -> None:
        self.HBNB_ENV = os.getenv('HBNB_ENV', "file")
        if self.HBNB_ENV == 'db':
            self.db_init()

    def db_init(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS model_name (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    data TEXT)''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def insert_model(self, name, data):
        try:
            self.cursor.execute("INSERT INTO model_name (name, data) VALUES (?, ?)", (name, data))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_all_db(self, model_name: str) -> list:
        try:
            self.cursor.execute(f"SELECT * FROM {model_name}")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def get_db(self, model_name: str, obj_id: str):
        try:
            self.cursor.execute(f"SELECT * FROM {model_name} WHERE id=?", (obj_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def save(self, table_name, data):
        if 'id' in data and self.get_by_id(table_name, data['id']):
            # Construct the SQL update statement
            set_clause = ', '.join([f"{key} = ?" for key in data if key != 'id'])
            sql_statement = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
            values = [data[key] for key in data if key != 'id'] + [data['id']]
        else:
            # Construct the SQL insert statement
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            sql_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            values = list(data.values())

        try:
            self.cursor.execute(sql_statement, values)
            self.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()

    def get_by_id(self, table_name, record_id):
        """
        Check if a record exists by ID.

        :param table_name: The name of the table.
        :param record_id: The ID of the record.
        :return: True if the record exists, False otherwise.
        """
        sql_statement = f"SELECT * FROM {table_name} WHERE id = ?"
        self.cursor.execute(sql_statement, (record_id,))
        return self.cursor.fetchone() is not None

    def update_model(self, obj_id: str, name: str, data: str):
        try:
            self.cursor.execute("UPDATE model_name SET name=?, data=? WHERE id=?", (name, data, obj_id))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_model(self, obj_id: str):
        try:
            self.cursor.execute("DELETE FROM model_name WHERE id=?", (obj_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def close_connection(self):
        self.connection.close()
