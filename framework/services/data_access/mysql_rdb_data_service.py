# app/services/data_access/mysql_rdb_data_service.py

import mysql.connector
from framework.services.data_access.base_data_service import BaseDataService

class MySQLRDBDataService(BaseDataService):
    def __init__(self, config):
        super().__init__(config)
        self.connection = self._get_connection()

    def _get_connection(self):
        db_host = self.config.get_config("DB_HOST")
        db_user = self.config.get_config("DB_USER")
        db_password = self.config.get_config("DB_PASSWORD")
        db_name = self.config.get_config("DB_NAME")

        connection = mysql.connector.connect(host=db_host, user=db_user,
                                             password=db_password,
                                             database=db_name)
        return connection

    def get_data_object(self, database_name, collection_name, key_field,
                        key_value):
        cursor = self.connection.cursor(dictionary=True)
        query = f"SELECT * FROM {collection_name} WHERE {key_field} = %s"
        cursor.execute(query, (key_value,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def create_data_object(self, database_name, collection_name, data):
        cursor = self.connection.cursor()
        keys = ', '.join(data.keys())
        values_placeholder = ', '.join(['%s'] * len(data))
        query =(f"INSERT INTO {collection_name} ({keys}) VALUES "
                f"({values_placeholder})")
        cursor.execute(query, tuple(data.values()))
        self.connection.commit()
        cursor.close()

    def update_data_object(self, database_name, collection_name, key_field,
                           key_value, data):
        cursor = self.connection.cursor()
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        query = (f"UPDATE {collection_name} SET {set_clause} "
                 f"WHERE {key_field} = %s")
        params = tuple(data.values()) + (key_value,)
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def delete_data_object(self, database_name, collection_name, key_field,
                           key_value):
        cursor = self.connection.cursor()
        query = f"DELETE FROM {collection_name} WHERE {key_field} = %s"
        cursor.execute(query, (key_value,))
        self.connection.commit()
        cursor.close()
