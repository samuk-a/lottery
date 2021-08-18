import datetime
from datetime import date

import requests
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from classes.database import Database
from classes.utils import Utils
from models.tables import Lotofacil

load_dotenv(find_dotenv())

Utils.load_config()

def lotofacil():
	resp = requests.get('http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/')
	print('Get')
	df = pd.read_html(resp.text)[0]
	print('Parse')
	lotofacil = Lotofacil()
	db = Database(auto_commit=False)
	db.create_table(lotofacil)
	for _, row in df.iterrows():
		data = datetime.datetime.strptime(row['Data Sorteio'], "%d/%m/%Y")
		values = [row['Concurso'], data.date().isoformat(), [row[f'Bola{i}'] for i in range(1, 16)]]
		db.insert(lotofacil, values)
	print('Inserted')
	db.commit()

if __name__ == '__main__':
	lotofacil()
