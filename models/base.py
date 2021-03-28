from typing import List

from pydantic import BaseModel


class ColumnBase(BaseModel):
    name: str
    type: type
    max_length: int = 255
    is_null: bool = True
    is_primary: bool = False

    def parse_attr(self):
        _type = ""
        if self.type == str:
            _type = f'VARCHAR({self.max_length})'
        elif self.type == int:
            _type = 'INT'
        elif self.type == bool:
            _type = 'BOOLEAN'

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
        print(sql)
        return sql
