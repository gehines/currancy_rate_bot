import requests
import json
from config import keys


class APIException(Exception):
  pass


class СurrencyConverter:
  @staticmethod
  def get_price(quote: str, base: str, amount: str):
    if quote == base:
      raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

    try:
      quote_ticker = keys[quote]
    except KeyError:
      raise APIException(f'Не удалось обработать валюту {quote}')

    try:
      base_ticker = keys[base]
    except:
      raise APIException(f'Не удалось обработать валюту {base}')

    try:
      amount = float(amount)
    except:
      raise APIException(f'Не удалось обработать количество {amount}')

    url = (f"https://api.apilayer.com/exchangerates_data/convert?to={keys[quote]}&from={keys[base]}&amount={amount}")
    payload = {}
    headers = {
      "apikey": "4r6QC0fpaowi6gD6J8516DXibOpIWQ0b"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    status_code = response.status_code
    total_base = json.loads(response.content)["result"]

    return total_base