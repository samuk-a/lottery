from datetime import date
from typing import List

from models.base import TableBase, ColumnBase


class Lotofacil(TableBase):
	name: str = 'lotofacil'
	columns: List[ColumnBase] = [
		ColumnBase(name="contest", type=int, is_primary=True),
		ColumnBase(name="date", type=date, is_null=False),
		ColumnBase(name="balls", type=int, max_length=15, is_array=True, is_null=False)
	]