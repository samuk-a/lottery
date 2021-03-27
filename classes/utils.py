import os
from json import loads


class Utils:
    @staticmethod
    def load_config():
        try:
            path = os.getenv('CONFIG_FILE')
            with open(path) as f:
                dicio = loads(f.read())
                for k, v in dicio.items():
                    Utils._jsonize(k, v)
        except Exception as e:
            print("Error while loading CONFIGS")
            print(e)
            exit(1)

    @classmethod
    def _jsonize(cls, key, value):
        if type(value) != dict:
            os.environ[key] = str(value)
            return
        for k, v in value.items():
            if type(value) == dict:
                k = f"{key}.{k}"
            cls._jsonize(k, v)