# from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup as bs
# from urllib.request import urlretrieve
from zipfile import ZipFile
from os import remove
import ssl
import warnings

# Issue handling
warnings.filterwarnings('ignore')  # 移除bs4的warning
ssl._create_default_https_context = ssl._create_unverified_context  # SSL


# PTT beauty
url = "https://www.ptt.cc/bbs/Beauty/M.1593154950.A.1AB.html"

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


# Remove(extract) imgur圖片 ----------------------------
# 1. 第一個部分，連結
img_l = []
photo_hrefs = main_content.find_all("a")
for pic in photo_hrefs:
    if 'imgur' in pic["href"] and 'https' in pic["href"]:
        img_l.append(pic["href"])
        pic.extract()
# # 2. 第二個部分，圖片顯示(richcontent)
# richcontents = main_content.find_all("div", class_="richcontent")
# for rich in richcontents:
#    rich.extract()


for (m, v) in zip(metas, m_values):
    print(m.text, ':', v.text)


print("分數 :", score)
print("內文 :")

# print(main_content.text)
content = main_content.text
# content_split = content.split('--')
origin_content = content.split('--')[0]
ori_l = origin_content.split("\n")
ori_linted = []
for o in ori_l:
    if o != "":
        ori_linted.append(o)
for i in ori_linted:
    print(i)

print("圖片連結 :")
for img in img_l:
    # # 下載圖片
    # urlretrieve(img, img.split('/')[-1])
    print(img)

# 壓成zip檔，以推文數+照片張數命名，壓縮完成後刪除圖片
with ZipFile('PTTBeauty_'+str(score)+'_'+str(len(img_l))+'.zip', 'w') as myzip:
    for img in img_l:
        filename = img.split('/')[-1]
        myzip.write(filename)
        remove(filename)
