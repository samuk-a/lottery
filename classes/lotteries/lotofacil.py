from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from classes.database import Database
from models.base import Contest
from models.tables import Lotofacil as LotofacilModel


class Lotofacil:
	def __init__(self):
		self.url = 'https://www.sorteonline.com.br/lotofacil/resultados'
		self.contests: List[Contest] = []

	def crawl(self):
		session = requests.Session()
		resp = session.get(self.url)
		bs = BeautifulSoup(resp.text, "lxml")
		numbers = bs.find("div", {"class": "result result-default center"}).find_all('li', {'class': 'bg'})
		data = bs.find('span', {'class': 'color header-resultados__datasorteio'}).text.strip()
		contest = bs.find('span', {'id': 'nroConcursoHeader[0]'}).text.strip()

		numbers = [int(x.text.strip()) for x in numbers]
		data = datetime.strptime(data, '%d/%m/%Y')
		self.save(contest, data, numbers)

	def save(self, contest: int, data: datetime, balls: list):
		try:
			lotofacil = LotofacilModel()
			db = Database()
			values = [contest, data.date().isoformat(), balls]
			db.insert(lotofacil, values)
		except Exception as e:
			print(f'Error {e}')

	def select(self):
		try:
			lotofacil = LotofacilModel()
			db = Database()
			contests = db.select_all(lotofacil)
			for row in contests:
				self.contests.append(Contest(
					contest=row[0],
					date=row[1],
					balls=row[2]
				))
			return self
		except Exception as e:
			print(f'Error {e}')


if __name__ == '__main__':
	Lotofacil().crawl()

