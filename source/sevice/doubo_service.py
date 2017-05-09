import urllib
from urllib.request import urlopen


def init():
    f = open("D:\python_work\yungou\\resources\category_img_url.txt", "r", encoding="utf8")
    url_list = []
    for line in f:
        l = line.replace("\n", "").split(",")
        url_list.append(l)
    return url_list


def down_load():
    url_list = init()
    head_url = "http://resources.sibu.cn/resource/load?path="
    for l in url_list:
        url = head_url + l[2]
        data = urllib.request.urlopen(url).read()
        name = 'D:\\temp\\' + l[0] + "_" + l[1].replace("/", "") + url[-4:-1] + "g"
        try:
            f = open(name, "wb")
            f.write(data)
        except:
            f.close()
