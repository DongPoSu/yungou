# -*- coding: UTF-8 -*-
import requests


# 查询秒杀
def query_spike_goods():
    result = requests.get("http://kuaigouapi.sibu.cn/quick/wave/queryWaveActivity")
    data = result.json()
    if (result.status_code == 200):
        good_info_list = dict(data).get("QuickBaseResponse").get("waveActivityList")
        for i in good_info_list:
            print(i)
    else:
        print(data)


# 删除秒杀商品
def delete_spike_good(date):
    result = requests.get("http://kuaigouapi.sibu.cn/quick/wave/deleteWaveActivity?date=%s" % (date))
    print(result.json())


# 删除缓存
def clear_spike_goods_cache(skuids):
    if (skuids is None):
        print("skuids is none")
    skuid_list = skuids.replace("@", ",").split(",")
    for i in skuid_list:
        result = requests.get("http://kuaigouapi.sibu.cn/quick/tool/deletegooddetail?goodsSkuId=%s" % (i))
        print(result.json())


# 添加秒杀产品
def add_spike_good(goods, date):
    result = requests.get("http://kuaigouapi.sibu.cn/quick/wave/addWaveActivity?date=%s&goodIdsInfo=%s" % (date, goods))
    if (result.status_code == 200):
        clear_spike_goods_cache(goods)
    else:
        print(result.json())


add_spike_good(
    "74048,74191,68219,74184,69695@70059,74185,74187,65469,70081@61829,74046,69755,74189,6843@65585,62031,68315,70077,65021",
    "2016-09-20", ),
query_spike_goods()
# delete_spike_good("2016-05-30")
