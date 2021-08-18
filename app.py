from dotenv import load_dotenv, find_dotenv
from classes.lotteries.lotofacil import Lotofacil
from classes.utils import Utils

load_dotenv(find_dotenv())
Utils.load_config()


def lotofacil():
	loto = Lotofacil()
	loto.crawl()
	return Utils.freq([x.balls for x in loto.select().contests])


if __name__ == "__main__":
	print(lotofacil())
