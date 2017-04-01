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
    result = requests.get("%s/quick/tool/deletemiaosha" % (host))
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

# clear_spike_goods_cache("64745,70055,70019,73265,69379@64797,70071,73967,69357,64713@73965,67819,69811,64983,69671@63793,65905,68439,69755,67805")
add_spike_good(
    "73965,73993,69365,67805,70057@65327,65905,73967,69585,70081@66115,74950,69345,74862,75491@69417,62031,68315,65021,75662",
    "2016-12-17")
# query_spike_goods()
# delete_spike_good("2016-12-09")





