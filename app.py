from dotenv import load_dotenv, find_dotenv

from classes.database import Database
from classes.utils import Utils
from models.base import TableBase

if __name__ == "__main__":
    load_dotenv(find_dotenv())

    Utils.load_config()
    lotofacil = TableBase(
        name="lotofacil"
    )
    Database().create_table(lotofacil)
