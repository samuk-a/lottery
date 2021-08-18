from typing import List
import datetime as dt

from pydantic import BaseModel


class ColumnBase(BaseModel):
    name: str
    type: type
    max_length: int = 255
    is_array: bool = False
    is_null: bool = True
    is_primary: bool = False

    def parse_attr(self):
        _type = ""
        if self.type == str:
            _type = f'VARCHAR({self.max_length})'
        elif self.type == int:
            _type = 'INTEGER'
        elif self.type == bool:
            _type = 'BOOLEAN'
        elif self.type == dt.datetime:
            _type = 'TIMESTAMP'
        elif self.type == dt.date:
            _type = 'DATE'

        if self.is_array:
            _type += f' ARRAY[{self.max_length}]'

        if self.is_primary:
            self.is_null = False
            _type += ' PRIMARY KEY'

        _type += (' NOT' if not self.is_null else '') + ' NULL'
        return _type


class TableBase(BaseModel):
    name: str
    columns: List[ColumnBase] = [ColumnBase(name="id", type=int, is_primary=True)]

    def create_sql(self, drop: bool = False):
        sql = '' if not drop else f'DROP TABLE IF EXISTS {self.name}; '
        cols = []
        for col in self.columns:
            cols.append(f'{col.name} {col.parse_attr()}')
        sql += f'CREATE TABLE {self.name} ({",".join(cols)})'
        return sql

    def insert_sql(self, values: list):
        values = ['%s' for _ in values]
        return f'INSERT INTO {self.name} VALUES ({",".join(values)})'

    def select_sql(self, cols: list = None, values: List[tuple] = None):
        cols = ", ".join(cols) if cols else "*"
        values = [f'{i} = {j}' for i, j in values] if values else ['1=1']
        return f'SELECT {cols} FROM {self.name} WHERE {" AND ".join(values)}'


class Contest(BaseModel):
    contest: int
    date: dt.date
    balls: List[int]