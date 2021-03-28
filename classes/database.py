from os import getenv
from postgres import Postgres

from models.base import TableBase


class Database:
    def __init__(self):
        _user = getenv("DATABASE.USER")
        _secret = getenv("DATABASE.PASS")
        _host = getenv("DATABASE.HOST")
        _port = getenv("DATABASE.PORT")
        _dbname = getenv("DATABASE.DB")
        self.db = Postgres(url=f"postgresql://{_user}:{_secret}@{_host}:{_port}/{_dbname}")

    def create_table(self, table: TableBase):
        self.db.run(table.create_sql(drop=True))