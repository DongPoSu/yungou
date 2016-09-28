import pymysql
import common.DbUtil as DbUtil
import common.StrUtil as StrUtil
import constants.db_constants as db_constants

# 扫描异常订单
def scan_exception_address():
    sql = "SELECT m.phone,m.user_name,a.member_id,a.province,a.city,a.district, a.detail FROM("
    for i in range(db_constants.TABLE_SIZE):
        sql += " SELECT * FROM member_address_" + StrUtil.format(i)
        if (i < db_constants.TABLE_SIZE -1):
            sql += " UNION ALL "
    sql += ")a join sibu_directsale.member m ON a.member_id = m.member_id " \
           "WHERE  (a.province LIKE'上海市' or a.province LIKE '天津市' or a.province LIKE '重庆市' or a.province LIKE '深圳市') and a.city='县'"
    print(sql)
    for i in range(db_constants.DB_SIZE):
        db_url = DbUtil.get_db_ip(i)
        module = StrUtil.format(i)
        table = "sibu_directsale_member_" + module
        db = pymysql.connect(db_url, "root", "Aa123456", table, charset = "utf8mb4")
        cursor = db.cursor()
        cursor.execute(sql)
        temp = cursor.fetchall()
        if (temp is not None):
            for i in temp:
                print(i)
        cursor.close()


def repair_member_address():
    result = 0
    for i in range(db_constants.DB_SIZE):
        db_url = DbUtil.get_db_ip(i)
        module = StrUtil.format(i)
        table = "sibu_directsale_member_" + module
        for i in range(db_constants.TABLE_SIZE):
            sql = " update member_address_" + StrUtil.format(i)
            sql += " a set a.province='北京', a.city='北京市'" \
                   " WHERE a.province LIKE '北京市' AND a.city LIKE '县' AND a.city NOT LIKE '市辖区'"
            db = pymysql.connect(db_url, "root", "Aa123456", table, charset="utf8mb4")
            cursor = db.cursor()
            result += cursor.execute(sql)
            if (result <= 0):
                continue
            try:
                db.commit()
                print("success: " + str(result))
            except:
                print(sql)
                db.rollback()
            db.close()

# scan_exception_address()
# repair_member_address()


