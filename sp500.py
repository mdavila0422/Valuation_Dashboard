import requests
import pandas as pd
from bs4 import BeautifulSoup

def sp500_stocks_info():
    #Make request to sp500 wiki page and parse html
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = BeautifulSoup(resp.text, 'lxml')

    #Search for table
    stocks_info = []
    tickers = []
    securities = []
    gics_sectors = []
    gics_sub_industries = []
    print("searching for sp500 companies")
    table = soup.find("table")
    #search table skipping header row
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        security = row.findAll('td')[1].text
        gics_sector = row.findAll('td')[3].text
        gics_sub_industry = row.findAll('td')[4].text
        
        tickers.append(ticker.lower().replace("\n", ""))
        securities.append(security)
        gics_sectors.append(gics_sector.lower())
        gics_sub_industries.append(gics_sub_industry.lower())

    stocks_info.append(tickers)
    stocks_info.append(securities)
    stocks_info.append(gics_sectors)
    stocks_info.append(gics_sub_industries)

    stocks_info_df = pd.DataFrame(stocks_info).T
    stocks_info_df.columns = ['tickers', 'security', 'gics_industry', 'gics_sub_industry']
    stocks_info_df['seclabels'] = 'SP500'
    stocks_info_df['labels'] = stocks_info_df[['tickers', 'security', 'gics_industry', 'gics_sub_industry', 'seclabels']].apply(lambda x: ' '.join(x), axis=1)

    dictlist = []
    for index, row in stocks_info_df.iterrows():
        dictlist.append({'value':row['tickers'], 'label': row['labels']})
    return dictlist

sp500_stocks_info()