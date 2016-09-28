# -*- coding: UTF-8 -*-
import requests

host = "http://kuaigouapi.sibu.cn"
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
        result = requests.get("%s/quick/tool/deletegooddetail?goodsSkuId=%s" % (host,i))
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
    "62043,74190,64983,74193,64713@62067,70037,68485,68219,65587@68211,69581,74194,65611,70057@69599,63703,69695,73969,64993",
    "2016-09-27")
query_spike_goods()
# delete_spike_good("2016-09-21")



















