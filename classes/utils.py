import os
from json import loads
from typing import List


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

    @staticmethod
    def freq(values: List[list]) -> dict:
        dicio = {}
        for row in values:
            for val in row:
                dicio.update({val: dicio.get(val, 0) + 1})
        return dict(sorted(dicio.items(), key=lambda item: item[1], reverse=True))
