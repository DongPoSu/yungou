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
    count = str(goods).count("@")
    if count is not 3:
        print("格式不正确！")
        return
    result = requests.get("http://kuaigouapi.sibu.cn/quick/wave/addWaveActivity?date=%s&goodIdsInfo=%s" % (date, goods))
    if result.status_code == 200:
        clear_spike_goods_cache(goods)
    else:
        print(result.json())


# add_spike_good(
#     "61895,66049,69365,69669,65361@66115,69353,69345,25898,69359@64797,68439,68387,66019,64713@70051,69363,70075,73970,69485",
#     "2016-09-21")
# query_spike_goods()
# delete_spike_good("2016-09-21")
