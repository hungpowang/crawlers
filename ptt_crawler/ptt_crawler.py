from urllib.request import urlopen, Request
# import requests
from bs4 import BeautifulSoup as bs

# 移除bs4的warning
import warnings
warnings.filterwarnings('ignore')

# for SSL issue of MacOS
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.ptt.cc/bbs/MuscleBeach/M.1592112509.A.BC5.html"

# 建立一個包含 Header 的完整 Request
# 1. New a request
r = Request(url)
# 2. Add header to request
user_agent= "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
r.add_header("user-agent", user_agent)

# 送出request，並且以response接收回應
response = urlopen(r)

# 若使用第三方套件‘requests’，則將建立req、加入header、送出req，改為下面一行
# response = requests.get(url).text

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