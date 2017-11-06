from bs4 import BeautifulSoup
import requests
import pandas as pd
from multiprocessing import Pool

url = 'https://gist.github.com/paulmillr/2657075'


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



def getTopContributors(url):

    soup = getSoupFromURL(url)
    x = {}

    for contributor in soup.find_all("th", scope='row'):
        x[int(contributor.parent.th.text.split('#')[1])] = contributor.parent.a.text
        try:
            print(contributor.parent.th.text.split('#')[1] + '  :  ' + contributor.parent.td.text.split('(')[1][:-1] )
        except IndexError:
            print(contributor.parent.th.text.split('#')[1] + '  :  ' + contributor.parent.a.text)
    return x


def getUserAverageStar(users):
    url = 'https://api.github.com/users/' + users + '/repos'
    r = requests.get(url, auth = ('DStromae','githubmdp8*'))
    if r.status_code == 200:
        star_average = pd.Series([repo['stargazers_count'] for repo in r.json()]).mean()
        return star_average
    else:
        return 'Authentification problem or user doesn\'t not exist'

if __name__ == '__main__':
    url = 'https://gist.github.com/paulmillr/2657075'
    Users = list(getTopContributors(url).values())

    p = Pool(450)
    print(type(p.map(getUserAverageStar,Users)))

    '''for user in Users:
        print(user,getUserAverageStar(user))'''
