from dotenv import load_dotenv, find_dotenv

from classes.utils import Utils

if __name__ == "__main__":
    load_dotenv(find_dotenv())

    Utils.load_config()
