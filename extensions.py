import requests
import json
from config import keys

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
            exchange_rate = json.loads(r.content)[keys[quote]]
            return f"{exchange_rate * float(amount):.2f}"
        except Exception as e:
            raise APIException(f"Ошибка при получении цены: {e}")

    @staticmethod
    def convert(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}. Проверетьте правильность написания валюты')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}. Проверетьте правильность написания валюты')

        return CurrencyConverter.get_price(base, quote, amount)
