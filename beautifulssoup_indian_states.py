'''
references:
http://www.dataschool.io/python-web-scraping-of-president-trumps-lies/#whatiswebscraping
https://www.analyticsvidhya.com/blog/2015/10/beginner-guide-web-scraping-beautiful-soup-python/
'''


import requests 
from bs4 import BeautifulSoup
import pandas as pd


wiki = "https://en.wikipedia.org/wiki/List_of_state_and_union_territory_capitals_in_India"
page = requests.get(wiki)
soup = BeautifulSoup(page.text, 'html.parser')
trow=soup.find_all('table', attrs={'class': "wikitable"})
data={}
columns=[]
for table in trow:
    
    ths=table.find_all('th', attrs={'scope': "col"})
    for th in ths:
        columns.append(th.text)
    rows=table.find_all('tr')
    i=0
    for row in rows:
        if i not in data.keys():
            data[i]=[]
        
        th=row.find('th')
        data[i].append(th.text)
        cols = row.find_all('td')
        j=0
        for col in cols:
            data[i].append(col.text)
            j=j+1
        if j < 6:
            for k in range(j, 6):
                data[i].append("")
                             
        i=i+1
del data[0]


columns=list(map(lambda x: x.replace(' ', '_').lower(), columns))
print (columns)
d=pd.DataFrame(data)
d=d.transpose()

d.columns=['1','2', '3','4','5', '6', '7']
d=d.drop('2', axis=1)
columns=columns[1:]
d.columns=columns
d.sort_values(['year_capital_was_established'], ascending=[1])

d.head()

