
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup




def construct_url(computer):
    return 'https://www.cdiscount.com/search/10/'+computer+'+pc+portable.html#_his_'


def getSoupFromURL(url, method='get', data={}):

  if method == 'get':
    res = requests.get(url)
  elif method == 'post':
    res = requests.post(url, data=data)
  else:
    return None

  if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup
  else:
    return None


def get_prices(soup):

    computer_df = []


    prix_barre = soup.findAll("div", class_='prdtPInfoT')
    prix_actuel = soup.findAll("div", class_='prdtPrice')


    for price_article_barre,price_article_actuel in zip(prix_barre,prix_actuel):

        computer_df.append({'name': price_article_actuel.parent.parent.previous_sibling.previous_sibling.text, 'prix_actuel': price_article_actuel.text, 'prix_precedent': price_article_barre.text})

    return pd.DataFrame(computer_df).replace('',np.nan).dropna(how='any')






def form_number_euro(x):
    tab = x.split('€')
    return int(tab[0])+0.01*int(tab[1])

def form_number_comma(x):
    tab = x.split(',')
    return int(tab[0])+0.01*int(tab[1])


def construct_dataframe(df):

    df['prix_actuel'] = pd.DataFrame(df)['prix_actuel'].apply(form_number_euro)
    df['prix_precedent'] = pd.DataFrame(df)['prix_precedent'].apply(form_number_comma)

    return df




def compute_rebates(dataframe):

    dataframe['rebates'] = (dataframe['prix_actuel']-dataframe['prix_precedent'])*100/dataframe['prix_precedent']
    return dataframe.sort(columns ='rebates')



def compare_prices(computer1,computer2):
    url_1 = construct_url('acer')
    url_2 = construct_url('dell')

    soup1 = getSoupFromURL(url_1, method='get', data={})
    soup2 = getSoupFromURL(url_2, method='get', data={})

    dataframe1 = get_prices(soup1)
    dataframe2 = get_prices(soup2)

    dataframe1 = construct_dataframe(dataframe1)
    dataframe2 = construct_dataframe(dataframe2)

    dataframe1 = compute_rebates(dataframe1)
    dataframe2 = compute_rebates(dataframe2)

    return  dataframe1, dataframe2



acer,dell = compare_prices('acer','dell')
print(acer)
