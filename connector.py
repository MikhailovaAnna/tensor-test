import psycopg2

from config import PG_DATABASE, PG_USER, PG_PASSWD, PG_HOST, PG_PORT


class Connector:
    def __init__(self):
        self.conn = self._get_connection()
        self.cur = self.conn.cursor()
        self.schema = 'TEST'
        self.table = 'test'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def _get_connection(self):
        """
            Соединение с тестовой БД
        :return connection:
        """
        return psycopg2.connect(
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWD,
            host=PG_HOST,
            port=PG_PORT
        )
