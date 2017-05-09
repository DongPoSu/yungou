import pymysql

import common.DbUtil as DbUtil
import common.StrUtil as StrUtil
import constants.db_constants as db_constants


# 复制流水号到 payment_number
def copy_tradenum(order_list):
    for i in order_list:
        module = DbUtil.get_mod_16(DbUtil.get_module_by_order_code(i))
        table_index = DbUtil.get_mode_64(DbUtil.get_module_by_order_code(i))
        db_url = DbUtil.get_db_ip(module)

        db = pymysql.connect(db_url, "root", "Aa123456", "sibu_directsale")
        cursor = db.cursor()
        sql = "SELECT t.trade_id\
              FROM sibu_directsale_order_log_%s.trade_log_%s t \
              WHERE t.order_code = '%s' ORDER BY create_date ASC  LIMIT 1" % (module, table_index, i)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result is None:
            print("failed: trade is none")
            continue
        elif result[0] is None or str(result[0]).startswith("T"):
            print("failed: " + i + "-" + result[0])
            continue

        sql = "UPDATE sibu_directsale_order_%s.doing_order_%s o SET o.payment_number = %s WHERE o.order_code = '%s'" % (
            module, table_index, result[0], i)
        cursor.execute(sql)
        try:
            db.commit()
            print("success: " + i + "-" + result[0])
        except:
            print("failed: " + i)
            db.rollback()
        db.close()





def search_order(price_start, price_end, start_date, end_date, is_pay):
    # 组装sql
    sql = "SELECT d.order_code, d.total_money,case when d.order_status=2 then 'haspay' WHEN d.order_status=1 THEN 'unpay' else 'other' end " \
          " from ({tables})d WHERE d.create_date >='{create_date_start}' AND d.create_date <='{create_date_end}' AND d.total_money >={price_start} " \
          "AND d.total_money <={price_end}  AND d.delete_flag =0 AND d.is_pay={is_pay} ORDER  BY d.create_date"
    table = ""
    for i in range(64):
        table += "select * from doing_order_" + StrUtil.format(i)
        if (i < 63):
            table += " UNION ALL "
    sql = sql.format(tables=table, create_date_start=start_date, create_date_end=end_date, price_start=price_start,
                     price_end=price_end, is_pay=is_pay)
    print(sql)
    for i in range(16):
        db_url = DbUtil.get_db_ip(i)
        module = StrUtil.format(i)
        table = "sibu_directsale_order_" + module
        db = pymysql.connect(db_url, "root", "Aa123456", table)
        cursor = db.cursor()
        cursor.execute(sql)
        temp = cursor.fetchall()
        if (temp is not None):
            print(temp)


def query_order(order_list):
    for i in order_list:
        sql = "SELECT order_code, order_status, express_id, express_code,address,ship_date from sibu_directsale_order_{module}.doing_order_{table_index} WHERE order_code='{order_code}'"
        module = DbUtil.get_mod_16(DbUtil.get_module_by_order_code(i))
        table_index = DbUtil.get_mode_64(DbUtil.get_module_by_order_code(i))
        db_url = DbUtil.get_db_ip(module)
        db = pymysql.connect(host=db_url, user="root", passwd="Aa123456", db="sibu_directsale", charset="utf8mb4")
        sql = sql.format(module=module, table_index=table_index, order_code=i)
        cursor = db.cursor()
        cursor.execute(sql)
        print(cursor.fetchall())
        db.close()


# 根据日志创建时间，更新流水号到订单pay_number
def update_trade_id_by_create(start_date, end_date):
    exec_trade_sql = 'SELECT a.order_code, a.trade_id FROM('
    for i in range(db_constants.TABLE_SIZE):
        index = StrUtil.format(i)
        exec_trade_sql += " SELECT * FROM trade_log_" + index
        if (i < db_constants.TABLE_SIZE - 1):
            exec_trade_sql += ' union all '
    exec_trade_sql += ")a WHERE a.trade_id NOT LIKE ('T%') AND a.create_date>='" + start_date + "' AND a.create_date<='" + end_date + "'"
    for i in range(db_constants.DB_SIZE):
        db_url = DbUtil.get_db_ip(StrUtil.format(i))
        db = pymysql.connect(host=db_url, user="root", passwd="Aa123456", db="sibu_directsale_order_log_" + StrUtil.format(i), charset="utf8mb4")
        cursor = db.cursor()
        cursor.execute(exec_trade_sql)
        update_order_trade(cursor.fetchall())
        cursor.close()


# 更新订单流水
def update_order_trade(list):
    for i in list:
        order_code = str(i[0])
        trade_id = str(i[1])

        module = DbUtil.get_mod_16(DbUtil.get_module_by_order_code(order_code))
        table_index = DbUtil.get_mode_64(DbUtil.get_module_by_order_code(order_code))
        db_url = DbUtil.get_db_ip(module)
        db = pymysql.connect(db_url, "root", "Aa123456", "sibu_directsale")
        cursor = db.cursor()
        sql = "UPDATE sibu_directsale_order_%s.doing_order_%s o SET o.payment_number = %s WHERE o.payment_number IS NULL AND o.order_code = '%s'" % (
            module, table_index, trade_id, order_code)
        result = cursor.execute(sql)
        if(result <= 0 ):
            print("订单流水号已经存在: %s" + order_code)
            continue
        try:
            db.commit()
            print("success:%s %s" %(order_code,trade_id))
        except:
            print("failed: " + order_code)
            db.rollback()
        db.close()


# 扫描没有 流水号的订单
def scanNoTradeIdOrder(start_date, end_date):
    exec_trade_sql = 'SELECT c.order_code FROM('
    for i in range(db_constants.TABLE_SIZE):
        index = StrUtil.format(i)
        exec_trade_sql += "SELECT * FROM sibu_directsale_order_%s.doing_order_"+index+" a WHERE a.payment_number IS NULL" \
                          " AND a.order_code NOT IN (select b.order_code " \
                          " FROM sibu_directsale_order_log_%s.trade_log_"+index+" b" \
                          " WHERE b.trade_id not LIKE 'T%')"
        if (i < db_constants.TABLE_SIZE - 1):
            exec_trade_sql += ' union all '
    exec_trade_sql += ") c where c.payment_number is null and c.pay_date>='" + start_date + "' AND c.pay_date<='" + end_date + "'"
    fo = open("resources/test.txt", "r+")
    for i in range(db_constants.DB_SIZE):
        module = StrUtil.format(i)
        db_url = DbUtil.get_db_ip(module)
        db = pymysql.connect(host=db_url, user="root", passwd="Aa123456",db="sibu_directsale", charset="utf8mb4")
        cursor = db.cursor()
        cursor.execute(exec_trade_sql.replace("%s", module))
        result = cursor.fetchall()
        for i in result:
            fo.write(i[0] + "\n")

# scanNoTradeIdOrder("2016-08-30 00:00:00", "2016-08-31 23:59:59")
# read = open("test.txt", "r+")
# write = open("resources/result.txt", "r+")
#
# for line in open("test.txt"):
#     line = read.readline()
#     write.write(line[0:17] +"\n")
