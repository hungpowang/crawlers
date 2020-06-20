from urllib import request as rq
import json
import os

# for MAC computer only
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

for month in range(12):
    #src = "https://www.google.com/doodles/json/2020/5?hl=zh_TW"
    src = "https://www.google.com/doodles/json/2019/" + str(month + 1) + "?hl=zh_TW"
    with rq.urlopen(src) as resp:
        data = json.load(resp)
    for dic in data:
        # 在doodles資料夾下面建立每個月分的資料夾
        dir_name = "doodles/" + str(month + 1) + "/"
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        file_name = dir_name + dic['url'].split('/')[-1]
        file_url = 'https:' + dic['url']
        #with rq.urlopen(file_url) as resp:
        #    img = resp.read()
        #with open(file_name, 'wb') as doo_file:
        #    doo_file.write(img)
        rq.urlretrieve(file_url, file_name)