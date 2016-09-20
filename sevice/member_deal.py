# coding=utf8
from common import DbUtil
from common import StrUtil
from constants import db_constants
from constants.db_constants import BILL_DEAL
from dao import Deal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def init_sql(start_date, end_date, apply_type):
    sql = " SELECT  m.user_name,d.deal_code,d.apply_member_id, d.apply_date, d.apply_type, d.deal_status, " \
          " d.apply_money * 0.01 apply_money,d.give_invoice,d.check_date," \
          " CASE d.deal_status WHEN 2 THEN '审核通过' WHEN 5 THEN  '打款失败' WHEN 8 THEN '打款成功' ELSE '' END deal_status," \
          " c.bank_account,d.give_date," \
          " CASE c.bank_id" \
          " WHEN 1 THEN CONCAT('建行',c.bankcard_address)" \
          " WHEN 2 THEN CONCAT('农行',c.bankcard_address)" \
          " WHEN 3 THEN CONCAT('工行',c.bankcard_address)" \
          " WHEN 4 THEN CONCAT('中行',c.bankcard_address) ELSE '' END  bankcard_address," \
          " c.bank_user, c.bankcard_province, c.bankcard_city, c.bankcard_area," \
          " CASE c.bank_id WHEN 3 THEN '0200' ELSE '0000' END AS bank_id,m.phone" \
          " FROM sibu_directsale_profit_{db_index}.member_deal d " \
          " LEFT JOIN sibu_directsale_member_{db_index}.member_account c ON d.apply_member_id = c.member_id " \
          " LEFT JOIN sibu_directsale.member m ON m.member_id = d.apply_member_id"
    if apply_type is BILL_DEAL:
        where_sql = " WHERE d.check_date >= '%s' AND d.check_date <='%s' AND d.apply_type =%d AND d.deal_status = 2" % (
            start_date, end_date, apply_type)
    else:
        where_sql = " WHERE d.give_date >= '%s' AND d.give_date <= '%s' AND d.apply_type =%d " % (
            start_date, end_date, apply_type)
    return sql + where_sql


def query_deal(start_date, end_date, apply_type):
    deals = list()
    db_url = "mysql+pymysql://root:Aa123456@{ip}:3306/sibu_directsale"
    sql = init_sql(start_date, end_date, apply_type)
    for i in range(db_constants.DB_SIZE):
        db_index = StrUtil.format(i)
        ip = DbUtil.get_db_url(db_index)
        session = get_db_session(db_url, ip)
        exc_sql = sql.format(db_index=db_index)
        print(exc_sql)
        # try:
        result = session.query(Deal.BillDeal) \
            .from_statement(exc_sql).all()
        deals.extend(result)
        # except BaseException as err:
        #     print(err)
        session.close()
    return deals


def get_db_session(db_url, ip):
    # 初始化数据库连接:
    engine = create_engine(db_url.format(ip=ip), connect_args={'charset': 'utf8'}, echo=True)
    # 创建DBSession类型:
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session
