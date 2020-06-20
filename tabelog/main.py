from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pandas as pd

# for MacOS SSL issue
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# New an empty DataFrame
df = pd.DataFrame(columns=["店名", "評分", "日間價位", "夜間價位", "Blog"])

page = 57   # starting page
while True:
    url = "https://tabelog.com/tokyo/rstLst/" + str(page) + "/"
    try:
        response = urlopen(url)
        html = BeautifulSoup(response)
        print("\nPage[ {} ] is as below." .format(page))
    except HTTPError:
        print("\nAbove one is the last page!")
        break

    # 想抓取的欄位 [店名, 評分, 日間價位, 夜間價位, Blog]
    resturants = html.find_all("div", class_="list-rst__body")
    # type of "html":  <class 'bs4.BeautifulSoup'>
    # type of "resturants": <class 'bs4.element.ResultSet'> ...... LIST

    for r in resturants:
        names = r.find('a', class_="list-rst__rst-name-target cpy-rst-name")
        # type of names: <class 'bs4.element.Tag'>

        # deal with the missing rating
        try:
            rating = r.find('span', class_="c-rating__val c-rating__val--strong list-rst__rating-val")
            rating_score = rating.text
        except:     # In case there is no rating attribute
            rating_score = '-'

        night_price = r.find('span', class_="c-rating__val list-rst__budget-val cpy-dinner-budget-val")
        day_price = r.find('span', class_="c-rating__val list-rst__budget-val cpy-lunch-budget-val")
        print(names.text, rating_score , day_price.text, night_price.text, names["href"])

        # assamble data from series to DataFrame
        s = pd.Series([names.text, rating_score, day_price.text, night_price.text, names["href"]],
                           index=["店名", "評分", "日間價位", "夜間價位", "Blog"])
        df = df.append(s, ignore_index=True)

    page += 1

# export csv
df.to_csv("tabelog.csv", encoding='utf-8', index=False)
