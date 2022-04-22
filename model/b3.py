import yfinance as yf
from data_extractor import *


"""Classe Repository é responsável por armezar os dados dos papéis dos usuários, de forma não
redundante"""


class Repository:
    def __init__(self):
        self._list_asset = []

    def download_b3(self, ticker, period='5d'):
        if ticker in self._list_asset:
            return True
        else:
            data_b3 = yf.download(ticker, period=period, interval='1d', auto_adjust=True)
            asset = Asset(ticker, data_b3['Close'])
            self._list_asset.append(asset)

    @property
    def list_asset(self):
        return self._list_asset





"""A classe Asset é definida como o cadastro do papel, seus principais métodos são: 
        - Calcular rentabilidade
        - """


class Asset:
    @staticmethod
    def add_name_asset(ticker):
        new_name = yf.Ticker(ticker).info['longName']
        write_database(ticker, new_name)
        return new_name
    """ data b3 precisa ser 'Close' """
    def __init__(self, ticker, data_b3):
        self._ticker = ticker
        self._long_name = read_database(ticker[:-3]) if ticker[:-3] in read_database() else self.add_name_asset(ticker)
        self._price_today = {}
        self._price_back = {}
        self._profit = 0

        self._update_history(data_b3)
        self._update_profit()

    def _update_history(self, data_b3):
        self._price_back['date'] = data_b3.index[-2].to_pydatetime()
        self._price_today['date'] = data_b3.index[-1].to_pydatetime()
        self._price_back['price'] = data_b3[-2]
        self._price_today['price'] = data_b3[-1]

    def _update_profit(self):
        self._profit = (self._price_today['price'] - self._price_back['price'])/self._price_today['price']

    @property
    def ticker(self):
        return self._ticker

    @property
    def long_name(self):
        return self._long_name

    @property
    def profit(self):
        return self._profit

    def __eq__(self, other):
        return other == self._ticker
