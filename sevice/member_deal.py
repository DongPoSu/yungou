# coding=utf8
from common import DbUtil
from common import StrUtil
from common.DealStatus import PAY_SUCCESS, PAY_FAILED
from constants import db_constants
from constants.db_constants import BILL_DEAL
from dao import Deal




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
        where_sql = " WHERE d.delete_flag=0 and d.check_date >= '%s' AND d.check_date <='%s' AND d.apply_type =%d AND d.deal_status = 2" % (
            start_date, end_date, apply_type)
    else:
        where_sql = " WHERE d.delete_flag=0 and d.give_date >= '%s' AND d.give_date <= '%s' AND d.apply_type =%d " % (
            start_date, end_date, apply_type)
    return sql + where_sql


def query_deal(start_date, end_date, apply_type):
    deals = list()
    db_url = "mysql+pymysql://root:Aa123456@{ip}:3306/sibu_directsale"
    sql = init_sql(start_date, end_date, apply_type)
    for i in range(db_constants.DB_SIZE):
        db_index = StrUtil.format(i)
        ip = DbUtil.get_db_ip(db_index)
        session = DbUtil.get_db_session(ip)
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





def check_bank_deal(deal_result):
    # 查询member_id
    for i in range(db_constants.DB_SIZE):
        db_index = StrUtil.format(i)
        reuslt_list = query_member_id(db_index, deal_result)
        if len(reuslt_list) != 0:
            update_bank_deal(db_index, reuslt_list)

def query_member_id(db_index, deals):

    ip = DbUtil.get_db_ip(db_index)
    session = DbUtil.get_db_session(ip=ip)
    exc_sql = "SELECT c.member_id,d.deal_id"\
    " FROM" \
    " sibu_directsale_member_{db_index}.member_account c" \
    " JOIN sibu_directsale_profit_{db_index}.member_deal d ON c.member_id = d.apply_member_id"\
    " WHERE c.bank_account = '{bank_account}'" \
    " AND c.bank_user = '{bank_user}'" \
    " AND d.apply_money = {apply_money}" \
    " AND d.apply_type = 1"
    result_list = []
    for deal in deals:
        result = session.query(Deal.BillDealResult) \
            .from_statement(exc_sql.format(db_index=db_index,bank_account=deal.bank_account,bank_user=deal.bank_user, apply_money=deal.apply_money)).first()
        if result is None:
            continue
        deal.deal_id = result.deal_id
        deal.member_id = result.member_id
        result_list.append(deal)
    for d in result_list:
        deals.remove(d)
    session.close()
    return result_list

def update_bank_deal(db_index, deals):
    for deal in deals:
        if deal.deal_status == PAY_SUCCESS:
            update_success(db_index,deal)
        # elif deal.deal_status == PAY_FAILED:
            # update_failed(db_index, deal)

def update_success(db_index,deal):
    exec_sql = "UPDATE sibu_directsale_profit_%s.member_deal SET"\
    " deal_status = %d," \
    " update_date = now()," \
    " give_user_id = 1," \
    " give_date = now()," \
    " give_invoice = '%s'," \
    " service_charge_money = 0," \
    " proxy_tax_money = 0," \
    " back_money = 0," \
    " give_money = apply_money," \
    " deduct_tax_money = 0," \
    " remainder_money = 0" \
    " WHERE" \
    " delete_flag = 0" \
    " AND" \
    " deal_id  = '%s'" \
    " AND" \
    " deal_status = 2" % (db_index,deal.deal_status,deal.give_invoice,deal.deal_id)
    session = DbUtil.get_db_session(ip = DbUtil.get_db_ip(db_index))
    session.begin(subtransactions=True)
    try:
        result = session.execute(exec_sql)
        if(result.rowcount == 1):
            session.commit()
        else:
            session.rollback()
    except Exception as err:
        print(err)
        session.rollback()
    session.close()



def update_failed(db_index, deal):
    # 更新提现状态
    exec_deal_sql = "UPDATE sibu_directsale_profit_%s.member_deal SET" \
               " deal_status = %d," \
               " update_date = now()," \
               " give_user_id = 1," \
               " give_date = now()," \
               " give_invoice = '%s'," \
               " service_charge_money = 0," \
               " proxy_tax_money = 0," \
               " back_money = 0," \
               " give_money = apply_money," \
               " deduct_tax_money = 0," \
               " remainder_money = 0" \
               " WHERE" \
               " delete_flag = 0" \
               " AND" \
               " deal_id  = '%s'" \
               " AND" \
               " deal_status = 2" % (db_index,deal.deal_status, deal.give_invoice, deal.deal_id)
    profit_total_sql = "UPDATE sibu_directsale_profit_%s.member_profit_total " \
                       " SET available_money = available_money +%d," \
                       " deal_sum_money = deal_sum_money -%d  WHERE member_id ='%s'" % (db_index,deal.apply_money,deal.apply_money,deal.member_id)
    session = DbUtil.get_db_session(ip=DbUtil.get_db_ip(db_index))
    try:
        session.execute(exec_deal_sql)
        session.execute(profit_total_sql)
        session.commit()
    except:
        session.rollback()
    # 更新用户可用余额和提现总金额
    # 插入支出流水


def get_member_id(phone_list):
    session = DbUtil.get_db_session(ip=DbUtil.get_db_ip("master"))
    fo = open("../resources/text.txt", "w+")
    fo.write('[')
    for i in phone_list:
        result = session.execute("select member_id from sibu_directsale.member WHERE phone =%s"% i)
        print(result.cursor._rows[0][0])
        fo.write('\''+result.cursor._rows[0][0] +'\',')
    fo.write(']')
    fo.close()


def delete_member_deal(ids):
    sql = "UPDATE sibu_directsale_profit_{db_index}.member_deal d" \
          " SET d.delete_flag = 1" \
          " WHERE" \
          " d.deal_status IN (1,2)" \
          " AND d.apply_member_id IN {ids}"
    for db_index in range (db_constants.DB_SIZE):
        db_index = StrUtil.format(db_index)
        session = DbUtil.get_db_session(ip=DbUtil.get_db_ip(db_index))
        try:
            result = session.execute(sql.format(db_index=db_index, ids=ids[0]))
            session.commit()
        except:
            session.rollback()


def query_member_deal(ids):
    sql = " SELECT d.deal_code,d.apply_member_id,d.deal_status,d.delete_flag,d.apply_money*0.01 as apply_money,m.phone" \
          " FROM sibu_directsale_profit_{db_index}.member_deal d, sibu_directsale.member m" \
          " WHERE d.deal_status IN (1,2) " \
          " AND d.apply_member_id IN {ids} AND  m.member_id = d.apply_member_id"
    result_list = []
    for db_index in range(db_constants.DB_SIZE):
        db_index = StrUtil.format(db_index)
        session = DbUtil.get_db_session(ip=DbUtil.get_db_ip(db_index))
        result = session.query(Deal.BillDeal).from_statement(sql.format(db_index=db_index, ids=ids)).all()
        result_list.extend(result)
    for deal in result_list:
        print(deal.deal_code,deal.apply_member_id,str(deal.deal_status), str(deal.delete_flag),str(deal.apply_money),str(deal.phone))


