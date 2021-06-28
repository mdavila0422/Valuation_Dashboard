"""
A finance API class using the api from https://financialmodelingprep.com/developer/docs

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import json
from urllib.request import urlopen

class FinanceAPI():
    """
    Core Class
    """

    def __init__(self):
        #Initiate the object
        self.key = ''
        self.key_registered = False
        pass

    def registerKey_(self,key):
        #register API key to the object
        assert type(key) is str, "Key must be a string"
        self.key = str(key)
        self.key_registered = True

    def profile_data_(self, symbol):
        """
        Pulls the metrics data from the API for the given ticker symbol
        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'
        Returns
        -------
        None. Updates the self.profile with the data. 
        """  
        if not self.key_registered:
            print('API key is not registered yet.')
            return None

        url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={self.key}"
        response = urlopen(url)
        data = response.read().decode("utf-8")
        self.profile = json.loads(data)

    def ratios_data_(self, symbol):
        """
        Pulls the financial ratios data from the API for the given ticker symbol
        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'
        Returns
        -------
        None. Updates the self.ratios with the data. 
        """  
        if not self.key_registered:
            print('API key is not registered yet.')
            return None

        url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={self.key}"
        response = urlopen(url)
        data = response.read().decode("utf-8")
        self.ratios = json.loads(data)

    def financial_growth_data_(self, symbol):
        """
        Pulls the financial growth data from the API for the given ticker symbol
        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'
        Returns
        -------
        None. Updates the self.growth with the data. 
        """  
        if not self.key_registered:
            print('API key is not registered yet.')
            return None

        url = f"https://financialmodelingprep.com/api/v3/financial-growth/{symbol}?apikey={self.key}"
        response = urlopen(url)
        data = response.read().decode("utf-8")
        self.growth = json.loads(data)

    def historical_price_data_(self, symbol):
        """
        Pulls the historical daily prices with change and volume from the API for the given ticker symbol
        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'
        Returns
        -------
        None. Updates the self.historical_price with the data. 
        """  
        if not self.key_registered:
            print('API key is not registered yet.')
            return None

        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={self.key}"
        response = urlopen(url)
        data = response.read().decode("utf-8")
        self.historical_price = json.loads(data)

    def earnings_data_(self, symbol):
        """
        Pulls the historical daily prices with change and volume from the API for the given ticker symbol
        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'
        Returns
        -------
        None. Updates the self.earnings with the data. 
        """  
        if not self.key_registered:
            print('API key is not registered yet.')
            return None

        url = f"https://financialmodelingprep.com/api/v3/earnings-surprises/{symbol}?apikey={self.key}"
        response = urlopen(url)
        data = response.read().decode("utf-8")
        self.earnings = json.loads(data)
    
    def build_dict(self, symbol):
        """
        Builds a dictionary with a given ticker symbols
        
        Parameters
        ----------
        symbol : A ticker symbol (str) e.g. 'MSFT','FB','AAPL', or 'TWTR'
        Returns
        -------
        A dictionary with all the profile and metrics data pulled from the API
        """
        #pull data
        if not self.key_registered:
            print('API key is not registered yet.')
            return None
        
        self.profile_data_(symbol)
        self.ratios_data_(symbol)
        self.financial_growth_data_(symbol)
        self.historical_price_data_(symbol)
        self.earnings_data_(symbol)
        #Empty dict
        data_dict = {}
        #Symbol
        data_dict["symbol"] = symbol
        #profile data
        data_dict["profile"] = {}
        for k in self.profile[0].keys():
            data_dict["profile"][k] = self.profile[0][k]
        #financial ratios data
        data_dict["ratios"] = {}
        for k in self.ratios[0].keys():
            data_dict['ratios'][k] = self.ratios[0][k]
        #financial growth data
        data_dict["growth"] = {}
        for k in self.growth[0].keys():
            data_dict['growth'][k] = self.growth[0][k]
        #historical price data
        data_dict["historical_price"] = []
        for day in self.historical_price['historical']:
            price_data = {}
            for k in day.keys():
                price_data[k] = day[k]
            data_dict["historical_price"].append(price_data)
        #earnings data
        data_dict["earnings"] = []
        for day in self.earnings:
            earnings_data = {}
            for k in day.keys():
                earnings_data[k] = day[k]
            data_dict["earnings"].append(earnings_data)

        return data_dict

    def cols_numeric_(self):
        """
        Transofrms columns to numeric (float) wherever applicable
        """
        for c in self.df.columns:
            try:
                self.df[c] = self.df[c].apply(float)
            except ValueError:
                pass

    def replace_None_(self):
        """
        Replaces NoneType data by np.nan in the DataFrame
        """
        self.df.fillna(value=pd.np.nan, inplace=True)

    def build_dataframe(self, lst):
        """
        Builds a DataFrame with a given list of ticker symbols
        
        Parameters
        ----------
        lst : A list of ticker symbols (str) 
            e.g. ['MSFT','FB','AAPL','TWTR']
        Returns
        -------
        A Pandas DataFrame with all the data pulled from the API, 
        indexed by the symbol (company)
        """
        if not self.key_registered:
            print('API key is not registered yet.')
            return None

        data_companies = []
        for c in lst:
            data_companies.append(self.build_dict(c))
        #Build the dataframe
        self.df = pd.DataFrame(data_companies)
        #Convert to numeric columns wherever applicable
        self.replace_None()
        self.cols_numeric()    

    def bar_chart(self, var='price', **kwargs):
        plt.figure(figsize=(10,4))
        plt.title("{}".format(var), fontsize=18)
        plt.bar(x=self.df['companyName'], height=self.df[var], **kwargs)
        plt.xticks(fontsize=14, rotation=45)
        plt.yticks(fontsize=14)
        plt.ylabel(var, fontsize=16)
        plt.show()

    def line_chart(self, ):
        pass