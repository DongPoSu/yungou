# -*- coding: UTF-8 -*-
import requests

host = ""
# 查询秒杀
def query_spike_goods():
    result = requests.get("%s/quick/wave/queryWaveActivity" %(host))
    data = result.json()
    if (result.status_code == 200):
        good_info_list = dict(data).get("QuickBaseResponse").get("waveActivityList")
        for i in good_info_list:
            print(i)
    else:
        print(data)


# 删除秒杀商品
def delete_spike_good(date):
    result = requests.get("%s/quick/wave/deleteWaveActivity?date=%s" % (host,date))
    print(result.json())


# 删除缓存
def clear_spike_goods_cache(skuids):
    if (skuids is None):
        print("skuids is none")
    skuid_list = skuids.replace("@", ",").split(",")
    for i in skuid_list:
        result = requests.get("/quick/tool/deletegooddetail?goodsSkuId=%s" % (host,i))
        print(result.json())


# 添加秒杀产品
def add_spike_good(goods, date):
    count = str(goods).count("@")
    if count is not 3:
        print("格式不正确！")
        return
    result = requests.get("%s/quick/wave/addWaveActivity?date=%s&goodIdsInfo=%s" % (host,date, goods))
    if result.status_code == 200:
        print(result)
        clear_spike_goods_cache(goods)
    else:
        print(result.json())

add_spike_good(
    "73989,74154,74153,69357,64743@64745,74046,66029,68483,68415@64797,69355,74155,74157,70057@67807,69349,74156,64993,70011",
    "2016-09-26")
query_spike_goods()
# delete_spike_good("2016-09-21")















