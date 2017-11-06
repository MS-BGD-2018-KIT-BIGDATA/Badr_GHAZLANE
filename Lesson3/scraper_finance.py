#IMPORTATION DE PACKAGES
from bs4 import BeautifulSoup #Parcours du code source ( HTML ou CSS)
import requests #requeter la page web
import re #regex




def getSoupFromURL(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None




'''En analysant l'url on se rend compte que la structure est fixe et qu'il est simple de chnager l'année'''

for i in range(2010,2016):
    url = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice=" + str(i)
    soup = getSoupFromURL(url)


    res = soup.findAll('td', class_='libellepetit G')
    rowsABCD = [r.parent.select_one("td:nth-of-type(2)").text for r in res if re.search('= [ABCD]\Z', r.text)]
    d = {}
    d[i] = rowsABCD


    print(d[i])
