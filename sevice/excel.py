# coding=utf8

import os

from openpyxl import Workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common import DbUtil
from common import StrUtil
from constants import db_constants
from dao import Deal

BILL_DEAL = 1
NORMAL_DEAL = 0


def query_deal(apply_start_date, apply_end_date, apply_type):
    deals = list()
    db_url = "mysql+pymysql://root:Aa123456@{ip}:3306/sibu_directsale"
    sql = " SELECT  m.user_name,d.deal_code,d.apply_member_id, d.apply_date, d.apply_type, d.deal_status, " \
          " d.apply_money * 0.01 apply_money,d.give_invoice,d.check_date," \
          " CASE d.deal_status WHEN 2 THEN '审核通过' WHEN 5 THEN  '打款失败' WHEN 8 THEN '打款成功' ELSE '' END deal_status," \
          " c.bank_account," \
          " CASE c.bank_id" \
          " WHEN 1 THEN CONCAT('建行',c.bankcard_address)" \
          " WHEN 2 THEN CONCAT('农行',c.bankcard_address)" \
          " WHEN 3 THEN CONCAT('工行',c.bankcard_address)" \
          " WHEN 4 THEN CONCAT('中行',c.bankcard_address) ELSE '' END  bankcard_address," \
          " c.bank_user, c.bankcard_province, c.bankcard_city, c.bankcard_area," \
          " CASE c.bank_id WHEN 3 THEN '0200' ELSE '0000' END AS bank_id,m.phone" \
          " FROM sibu_directsale_profit_{db_index}.member_deal d " \
          " LEFT JOIN sibu_directsale_member_{db_index}.member_account c ON d.apply_member_id = c.member_id " \
          " LEFT JOIN sibu_directsale.member m ON m.member_id = d.apply_member_id" \
          " WHERE" \
          " d.apply_date >= '{apply_start_date}'" \
          " AND d.apply_date <= '{apply_end_date}'" \
          " AND d.apply_type = {apply_type}" \
          " AND d.deal_status = 2"

    for i in range(db_constants.DB_SIZE):
        db_index = StrUtil.format(i)
        ip = DbUtil.get_db_url(db_index)
        session = get_db_Session(db_url, ip)
        exc_sql = sql.format(db_index=db_index, apply_start_date=apply_start_date, apply_end_date=apply_end_date,
                             apply_type=apply_type)
        print(exc_sql)
        # try:
        result = session.query(Deal.BillDeal) \
            .from_statement(exc_sql).all()
        deals.extend(result)
        # except BaseException as err:
        #     print(err)
        session.close()
    return deals


def get_db_Session(db_url, ip):
    # 初始化数据库连接:
    engine = create_engine(db_url.format(ip=ip), connect_args={'charset': 'utf8'}, echo=True)
    # 创建DBSession类型:
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


# 导出发票提现打款
def export_bill_deal(apply_start_date, apply_end_date, title):
    deals = query_deal(apply_start_date, apply_end_date, BILL_DEAL)
    wb = Workbook()
    ws = wb.active
    head_line = ['序号', '币种', '金额', '收款人账号', '收款人名称', '收款账号开户行名称', '收款省份/收款银行',
                 '收款地市', '地区代码', '付款账号开户行名称', '付款人账号/卡号', '付款人名称 / 卡名称',
                 '汇款用途', '备注', '预约付款日期', '汇款方式', '收款账户短信通知手机号码', '自定义序号', '协议编号']
    ws.append(head_line)
    count = 0
    for deal in deals:
        count += 1
        ws.append([count, "人民币", deal.apply_money, deal.bank_account, deal.bank_user, deal.bankcard_address,
                   deal.bankcard_province,
                   deal.bankcard_city, deal.bank_id, "工行广州花都雅居乐支行", "广州思埠网络开发有限公司", "3602202119100259501", "", "代付款",
                   "", title, deal.phone, "", ""])

    file_path = "E:\\sibu_work\\思埠云购\提现打款\\20160919\\"
    if os.path.exists(file_path) is False:
        os.mkdir(file_path)
    wb.save("%s%s发票打款.xlsx" % (file_path, title))


# 导出提现
def export_deal(apply_start_date, apply_end_date, title):
    deals = query_deal(apply_start_date, apply_end_date, NORMAL_DEAL)
    wb = Workbook()
    ws = wb.active
    head_line = ['序号', '姓名', '手机号', '提现金额', '提现状态', '申请日期', '打款备注', '审核日期']
    ws.append(head_line)
    count = 0
    for deal in deals:
        count += 1
        ws.append(
            [count, deal.user_name, deal.phone, deal.apply_money, deal.deal_status, deal.apply_date.strftime('%Y-%m-%d %H:%M:%S'), deal.give_invoice,
             deal.check_date.strftime('%Y-%m-%d %H:%M:%S')])
    file_path = "E:\\sibu_work\\思埠云购\提现打款\\20160919\\"
    if os.path.exists(file_path) is False:
        os.mkdir(file_path)
    wb.save("%s%s提现打款.xlsx" % (file_path, title))
