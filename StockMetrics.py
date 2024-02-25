from time import sleep
import requests
from bs4 import BeautifulSoup
from lxml import etree
import numpy as np
import pandas as pd

tickerData = pd.read_csv('Cleaned_Tickers.csv')

prices = []
marketCaps = []
PE = []
EPS = []
ratio = []
divY = []
Vol = []

Tickers = tickerData.Tickers
Names = tickerData.Names
Sectors = tickerData.Sectors

for i in range(len(tickerData)):  # range(len(tickerData))
    ticker = Tickers[i]
    URL = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    print(i, ticker, URL)
    headers = {

    }
    content = requests.request('GET', URL, headers={'path': f'/quote/{ticker}?p={ticker}',
                                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 '
                                                                  'Safari/537.36',
                                                    'scheme': 'https',
                                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                                    'Cookie': 'tbla_id=6b642cc0-9ff6-4e67-aa31-1fdeea518b01-tuctae397ee; F=d=cSLEybE9vCX6.RRctEuA7W0H1q8dxhYYra0yu.oc59JM; PH=l=en-US; Y=v=1&n=2jl8gn6380s6n&l=00hj8_l08170l/o&p=f28vvin00000000&iz=400099&r=ee&intl=us; gam_id=y-hOSqWWFG2uJXh4mgLyiH4qY.WFYB27lZfasUHTGUGSecYd_PMQ---A; ucs=tr=1691402027000; OTH=v=2&s=2&d=eyJraWQiOiIwMTY0MGY5MDNhMjRlMWMxZjA5N2ViZGEyZDA5YjE5NmM5ZGUzZWQ5IiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiMkZHUVdRQzdISkxYSVVFTzJRTTdBVDZETk0iLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiI2WVo4akt0eVpwYTMifX0.8N_R8R5ufYVTxK_9Kwvf7ar27FkH4Vp1hzkrCZhuFVjQrf_0KgfILc3UQvog-kAWpgh1InAMHoH18mGkEpH4yfZTn_nT2s5NrD9hWNScBmtaXuub98ihCYNoVnsV2dULZYFdipXJDQ4aYpwyOeQqhepIJ6it89aRwjkFm1GXr4Q; T=af=QkNBQkJBJnRzPTE2OTI2NDcxMjMmcHM9TmpxeThMOEl3UHNfcUlkajhZMTY5Zy0t&d=bnMBeWFob28BZwEyRkdRV1FDN0hKTFhJVUVPMlFNN0FUNkROTQFhYwFBSU14TGUxSgFhbAFhYXJ0aV92YWliaGF2AXNjAWRlc2t0b3Bfd2ViAWZzAUhwTnlIcXBrbkZoVQF6egFUNzc0a0JBN0UBYQFRQUUBbGF0AVVoRm5rQgFudQEw&kt=EAAFn_5pi5sAS72qhesjXSH3w--~I&ku=FAALxkhH241oqEtbu.3qlAjNPA2U0urNsvmUty1qYD74p24gSlzkcCViMUzBtqWKTC07aYYbk0dEk4YlOvAqljsnSV8wUZUBpEeWo22FSA2_0h26tg_3xiX7EVc6xSqDCT47gekVVMG1HVnHSxhtglnVgXqDP0Me1ziNdCYx2zjDFg-~E; axids=gam=y-hOSqWWFG2uJXh4mgLyiH4qY.WFYB27lZfasUHTGUGSecYd_PMQ---A&dv360=eS1ZVXBPb2NWRTJ1R25kUHozZGtRRzFlNFZZaFB3UFJIblYuNTgwWU85NWo3MFlkbUVnRGw0UEwuSmhKUmwxT0UxQ01KMX5B; maex=%7B%22v2%22%3A%7B%22dadb9128%22%3A%7B%22lst%22%3A1698603940%2C%22ic%22%3A1%7D%7D%7D; GUC=AQEBCAFlQ7FlckIhlgSh&s=AQAAADZJQxbr&g=ZUJl1g; A1=d=AQABBGQS6mMCENyPKExEbHvh2Yj1EBa8aNgFEgEBCAGxQ2VyZVlQb2UB_eMBAAcIZBLqYxa8aNgID8BXLbruyzkQIrPOgM9IKgkBBwoBCw&S=AQAAAkQmK-LnA09xhHuN9Q4E7Qk; A3=d=AQABBGQS6mMCENyPKExEbHvh2Yj1EBa8aNgFEgEBCAGxQ2VyZVlQb2UB_eMBAAcIZBLqYxa8aNgID8BXLbruyzkQIrPOgM9IKgkBBwoBCw&S=AQAAAkQmK-LnA09xhHuN9Q4E7Qk; A1S=d=AQABBGQS6mMCENyPKExEbHvh2Yj1EBa8aNgFEgEBCAGxQ2VyZVlQb2UB_eMBAAcIZBLqYxa8aNgID8BXLbruyzkQIrPOgM9IKgkBBwoBCw&S=AQAAAkQmK-LnA09xhHuN9Q4E7Qk; gpp=DBAA; gpp_sid=-1; cmp=t=1700420968&j=0&u=1YNN; PRF=t%3DAAPL%252BWEC%252B%255EGSPC%26newChartbetateaser%3D1; __gpi=UID=00000cdb8650fcba:T=1700420969:RT=1700422041:S=ALNI_MZcG6j_95mgHOGFvLKM1tyq3m6zvA; __gads=ID=281786745495dc8c:T=1700422045:RT=1700422045:S=ALNI_MY19a0zNj7xmJIluuK4Ocoiz8Fwtg'

                                                    })
    sleep(5)
    soup = BeautifulSoup(content.text, 'html.parser')
    dom = etree.HTML(str(soup))
    # print(soup.text)
    try:
        price = dom.xpath(
            '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[1]/table/tbody/tr[1]/td[2]')[
            0].text
        mcap = dom.xpath(
            '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[1]/td[2]')[
            0].text
        pe = dom.xpath(
            '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[3]/td[2]')[
            0].text
        eps = dom.xpath(
            '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[4]/td[2]')[
            0].text
        divYd = dom.xpath(
            '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[2]/table/tbody/tr[6]/td[2]')[
            0].text
        vol = dom.xpath(
            '/html/body/div[1]/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div/div/div[2]/div[1]/table/tbody/tr[8]/td[2]')[
            0].text
        print(price, mcap, pe, eps, divYd, vol)
        if price != 'N/A':
            prices.append(float(str(price).replace(",", "")))
            marketCaps.append(mcap)
            EPS.append(float(str(eps).replace(",", "")))
            if pe != 'N/A':
                PE.append(float(str(pe).replace(",", "")))
                ratio.append(round(float(str(eps).replace(",", ""))/float(str(pe).replace(",", "")), 3))
            else:
                PE.append(-1)
                ratio.append(-1)
            if 'N/A' in divYd:
                divY.append(-1)
            else:
                div = float(str(divYd).split(sep='(')[1].split(sep='%')[0])
                divY.append(div)
            Vol.append(float(str(vol).replace(",", "")))

        else:
            print("WAH")
            raise Exception
    except:
        print(prices, marketCaps, PE, EPS, divY, Vol)
        print("Fail")
        prices.append(-1)
        marketCaps.append(-1)
        PE.append(-1)
        EPS.append(-1)
        ratio.append(-1)
        divY.append(-1)
        Vol.append(-1)
    sleep(3)

print(prices)
print(marketCaps)
print(PE)
print(EPS)
print(ratio)
print(divY)
print(Vol)
d = {'Ticker': Tickers,
     'Price': prices,
     'MCap': marketCaps,
     'PE': PE,
     'EPS': EPS,
     'Earnings_Yield': ratio,
     'Div_Yield': divY,
     'Volume': Vol}
df = pd.DataFrame(data=d)
df.to_csv('final1.csv')
