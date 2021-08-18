from os import getenv
from psycopg2 import connect

from models.base import TableBase


class Database:
    def __init__(self, auto_commit: bool = True):
        _user = getenv("DATABASE.USER")
        _secret = getenv("DATABASE.PASS")
        _host = getenv("DATABASE.HOST")
        _port = getenv("DATABASE.PORT")
        _dbname = getenv("DATABASE.DB")
        self.db = connect(database=_dbname, user=_user, password=_secret, host=_host, port=_port)
        self.auto_commit = auto_commit

    def commit(self):
        self.db.commit()

    def _execute(self, sql: str, values: list = None):
        try:
            if values is None:
                values = []
            cur = self.db.cursor()
            cur.execute(sql, values)
            if self.auto_commit:
                self.commit()
            cur.close()
        except Exception as error:
            print(error)
        finally:
            if self.db is not None:
                self.db.close()

    def _query(self, sql: str, values: list = None) -> list:
        cur = self.db.cursor()
        cur.execute(sql, values)
        return cur.fetchall()

    def select_all(self, table: TableBase, cols: list = None) -> list:
        return self._query(table.select_sql(cols))

    def create_table(self, table: TableBase):
        self._execute(table.create_sql(drop=True))
        return self

    def insert(self, table: TableBase, values: list):
        self._execute(table.insert_sql(values), values)
        return self