# Для API
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

# Подключение к API coinmarketcap
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a165ccbb-f145-4c37-8477-7071ff9a43ca',
}

session = Session()
session.headers.update(headers)

def ParseAll():
    # получение курса Доллара по АПИ от ЦБ
    try:
        response = Session().get('https://www.cbr-xml-daily.ru/latest.js')
        data = json.loads(response.text)
        USDprice = 1/data['rates']['USD']
    except:
        USDprice = 0

    # Получение курса Etherium
    try:
        # Сам запрос
        parameters = {
            'id': '1027'
        }
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        CryptoPrice = data['data']['1027']["quote"]['USD']['price']
    except:
        CryptoPrice = 0

    return round(CryptoPrice, 2), round(USDprice, 2)


def CryptoRates():

    try:
        # Сам запрос
        parameters = {
            'id': '52'
        }
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        XRPPrice = data['data']['52']["quote"]['USD']['price']
    except:
        XRPPrice = 0

    try:
        # Сам запрос
        parameters = {
            'id': '1'
        }
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        BitcoinPrice = data['data']['1']["quote"]['USD']['price']
    except:
        BitcoinPrice = 0

    try:
        # Сам запрос
        parameters = {
            'id': '1027'
        }
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        EtheriumPrice = data['data']['1027']["quote"]['USD']['price']
    except:
        EtheriumPrice = 0

    return round(XRPPrice, 2), round(BitcoinPrice, 2), round(EtheriumPrice, 2)

