#Web Scrapping All Links With Python
from bs4 import BeautifulSoup
import requests
URL = "https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
for link in soup.find_all('a', href = True):
    print (link.get('href'))
URL = "https://finance.yahoo.com/news/true-value-always-prevails-against-technological-advancement-141902215.html"
page2 =requests.get(URL)
soup = BeautifulSoup(page2.content, 'html.parser')
print(soup.text)


