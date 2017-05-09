# coding=utf-8
from common.Config import ENVIRONMENT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

YUN_PRE_ORDER_CODE = "Y"
LAST_CHAR_1 = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f")
LAST_CHAR_2 = (
    "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0a", "0b", "0c", "0d", "0e", "0f", "10", "11", "12",
    "13",
    "14", "15", "16", "17", "18",
    "19", "1a", "1b", "1c", "1d", "1e", "1f", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "2a", "2b",
    "2c",
    "2d", "2e", "2f", "30", "31", "32", "33", "34", "35", "36", "37",
    "38", "39", "3a", "3b", "3c", "3d", "3e", "3f", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "4a",
    "4b",
    "4c", "4d", "4e", "4f", "50", "51", "52", "53", "54", "55", "56",
    "57", "58", "59", "5a", "5b", "5c", "5d", "5e", "5f", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69",
    "6a",
    "6b", "6c", "6d", "6e", "6f", "70", "71", "72", "73", "74", "75",
    "76", "77", "78", "79", "7a", "7b", "7c", "7d", "7e", "7f", "80", "81", "82", "83", "84", "85", "86", "87", "88",
    "89",
    "8a", "8b", "8c", "8d", "8e", "8f", "90", "91", "92", "93", "94",
    "95", "96", "97", "98", "99", "9a", "9b", "9c", "9d", "9e", "9f", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7",
    "a8",
    "a9", "aa", "ab", "ac", "ad", "ae", "af", "b0", "b1", "b2", "b3",
    "b4", "b5", "b6", "b7", "b8", "b9", "ba", "bb", "bc", "bd", "be", "bf", "c0", "c1", "c2", "c3", "c4", "c5", "c6",
    "c7",
    "c8", "c9", "ca", "cb", "cc", "cd", "ce", "cf", "d0", "d1", "d2",
    "d3", "d4", "d5", "d6", "d7", "d8", "d9", "da", "db", "dc", "dd", "de", "df", "e0", "e1", "e2", "e3", "e4", "e5",
    "e6",
    "e7", "e8", "e9", "ea", "eb", "ec", "ed", "ee", "ef", "f0", "f1",
    "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "fa", "fb", "fc", "fd", "fe", "ff")

# 正式环境
db_ip = {
    "master": "192.168.1.210",
    "00-03": "192.168.1.208",
    "04-07": "192.168.1.209",
    "08-11": "192.168.1.211",
    "12-15": "192.168.1.229"
}

# UAT环境
uat_db_ip = "192.168.1.113"

table_mod_count = 64

db_mod_count = 16


# 取模16(根据会员ID)
def get_mod_16(member_id):
    member_id = str(member_id).lower()
    length = len(member_id)
    last_char = int(member_id[length - 1: length], 16)
    module = int(LAST_CHAR_1[last_char], 16) % db_mod_count
    if module < 10:
        return "0" + str(module)
    else:
        return str(module)


def get_mode_64(member_id):
    """
    取模64(根据会员ID)
    返回 string
    """
    member_id = str(member_id).lower()
    length = len(member_id)
    last_char = int(member_id[length - 2: length], 16)
    module = int(LAST_CHAR_2[last_char], 16) % table_mod_count
    if module < 10:
        return "0" + str(module)
    else:
        return str(module)


def get_module_by_order_code(order_code):
    """
    根据订单号取得会员ID的尾数2位
    返回string
    """
    if str(order_code).startswith(YUN_PRE_ORDER_CODE):
        offset = 1
    else:
        offset = 0
    prefix = str(order_code)[offset:3 + offset]
    return LAST_CHAR_2[int(prefix)]


def get_db_ip(module):
    if ENVIRONMENT == "uat":
        return uat_db_ip
    elif ENVIRONMENT == "product":
        if module == "master":
            return db_ip.get(module)
        module = int(module)
        if module >= 0 and module <= 3:
            return db_ip.get("00-03")
        elif module >= 4 and module <= 7:
            return db_ip.get("04-07")
        elif module >= 8 and module <= 11:
            return db_ip.get("08-11")
        elif module >= 12 and module <= 15:
            return db_ip.get("12-15")


def get_db_session(ip):
    db_url = "mysql+pymysql://root:Aa123456@{ip}:3306/sibu_directsale"
    # 初始化数据库连接:
    engine = create_engine(db_url.format(ip=ip), connect_args={'charset': 'utf8'}, echo=True)
    # 创建DBSession类型:
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session