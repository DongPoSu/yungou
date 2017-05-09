from common import DbUtil
from common import StrUtil
from constants import db_constants
from dao import Order


def get_lose_member_Sql():
    sql = " SELECT b.order_id,b.member_id,b.phone,b.order_code FROM (";
    for i in range(db_constants.TABLE_SIZE):
        sql += " SELECT * FROM sibu_directsale_order_{db_index}.doing_order_%s" % (StrUtil.format(i))
        if (i < db_constants.TABLE_SIZE - 1):
            sql += " UNION ALL"
    sql += " )b WHERE b.member_id not in (SELECT  m.member_id FROM sibu_directsale.member m)" \
           " GROUP BY b.member_id"
    return sql


def get_lose_member():
    '''
    扫描已经下单但是该用户在member表中不存在的member_id和iphone
    :return:
    '''
    sql = get_lose_member_Sql()
    order_list = list()
    for i in range(db_constants.DB_SIZE):
        db_index = StrUtil.format(i)
        ip = DbUtil.get_db_ip(db_index)
        session = DbUtil.get_db_session(ip)
        exc_sql = sql.format(db_index=db_index)
        print(exc_sql)
        result = session.query(Order.DoingOrder) \
            .from_statement(exc_sql).all()
        order_list.extend(result)
    for r in order_list:
        print("%s,%s,%s,%s" % (r.order_id, r.member_id, r.phone, r.order_code))


def get_tranfer_records():
    '''
    获取所有转入，转出记录
    :return:
    '''
    sql = get_tranfer_Sql()
    record_list = list()
    for i in range(db_constants.DB_SIZE):
        db_index = StrUtil.format(i)
        ip = DbUtil.get_db_ip(db_index)
        session = DbUtil.get_db_session(ip)
        exc_sql = sql.format(db_index=db_index)
        print(exc_sql)
        result = session.query(Order.TransferRecord) \
            .from_statement(exc_sql).all()
        record_list.extend(result)
    return record_list


def get_tranfer_Sql():
    sql = " SELECT b.transfer_code,b.transfer_id,b.transfer_money,b.out_user_name,b.out_phone,m.user_name in_user_name,m.phone in_phone, b.transfer_memo,b.create_time " \
          " FROM (SELECT a.transfer_code,a.transfer_id,a.transfer_money * 0.01 transfer_money, m.user_name out_user_name, m.phone out_phone, a.in_member_id," \
          " a.transfer_memo, a.create_time FROM ("
    for i in range(db_constants.TABLE_SIZE):
        sql += " SELECT * FROM sibu_directsale_profit_{db_index}.member_transfer_%s" % (StrUtil.format(i))
        if (i < db_constants.TABLE_SIZE - 1):
            sql += " UNION ALL"
    sql += ") a JOIN sibu_directsale.member m ON a.out_member_id = m.member_id WHERE a. STATUS = 1  group by a.transfer_code) b" \
           "  JOIN sibu_directsale.member m ON b.in_member_id = m.member_id group by b.transfer_code"
    return sql
