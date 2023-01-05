import requests
import json
from config import keys


class ConvertionExeption(Exception):
    pass


class ValueConveter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        quote.lower()
        base.lower()

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise ConvertionExeption(f"Не удалось обработать валюту {quote}")

        try:
            base_ticket = keys[base]
        except KeyError:
            raise ConvertionExeption(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f"не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}")
        total_base = json.loads(r.content)[keys[base]] * amount

        return total_base