#from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup as bs

# 移除bs4的warning
import warnings
warnings.filterwarnings('ignore')

# for SSL issue of MacOS
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.ptt.cc/bbs/Beauty/M.1592192249.A.177.html"
# 待處理： 原po回應推文尚未移除掉

#url = "https://www.ptt.cc/bbs/Gossiping/M.1592240936.A.510.html"
#url = "https://www.ptt.cc/bbs/MuscleBeach/M.1592112509.A.BC5.html"

jar = requests.cookies.RequestsCookieJar()
# 可把不同網頁的 cookie 設定進一個jar
jar.set("over18", "1", domain="www.ptt.cc")
# 將cookies加入request
response = requests.get(url, cookies=jar).text

# response為html格式，交由bs4解析
html = bs(response)

main_content = html.find("div", class_="bbs-screen bbs-content")

metas = main_content.find_all("span", class_="article-meta-tag")
m_values = main_content.find_all("span", class_="article-meta-value")

# Remove(extract) 作者 標題 時間 ------------------------
meta = main_content.find_all("div", class_="article-metaline")
for m in meta:
    m.extract()
# Remove(extract) 看板名稱 ------------------------------
right_meta = main_content.find_all("div", class_="article-metaline-right")
for single_meta in right_meta:
    single_meta.extract()

# Remove(extract) imgur圖片 ----------------------------
# 1. 第一個部分，連結
photo_hrefs = main_content.find_all("a")
for pic in photo_hrefs:
    if 'imgur' in pic["href"]:
        pic.extract()
# 2. 第二個部分，圖片顯示(richcontent)
richcontents = main_content.find_all("div", class_="richcontent")
for rich in richcontents:
    rich.extract()

# Remove(extract) 推文前   ------------------------------
datas = main_content.find_all("span", class_="f2")
for data in datas:
    data.extract()

# Remove(extract) 推文   --------------------------------
pushes = main_content.find_all("div", class_="push")
score = 0
for single_push in pushes:
    push_tag = single_push.find("span", class_="push-tag").text
    if '推' in push_tag:
        score += 1
    elif '噓' in push_tag:
        score -= 1
    single_push.extract()




for (m, v) in zip(metas, m_values):
    print(m.text, ':', v.text)

print("分數 :", score)

print(main_content.text)