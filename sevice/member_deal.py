# coding=utf8
import pymysql

from common import DbUtil
from common import StrUtil
from constants import db_constants
from openpyxl import writer

def query_member_deal(start_date, end_date):
    sql = " SELECT m.user_name, m.phone, CASE d.deal_status WHEN 2 THEN 	'审核通过' WHEN 5 THEN 	'打款失败' WHEN 8 THEN 	'打款成功' ELSE 	'' END as deal_status," \
          " CASE d.apply_type WHEN 1 THEN 	'银行卡' ELSE 	'微信' END AS apply_type," \
          " d.apply_date," \
          " d.apply_money * 0.01 apply_money," \
          " d.give_date," \
          " d.give_invoice," \
          " d.apply_member_id," \
          " CONCAT('`', c.bank_account) AS bankcard_account," \
          " c.bankcard_user,"\
          " c.bankcard_province," \
          " c.bankcard_city," \
          " c.bankcard_area," \
          " c.bankcard_address," \
          " CASE c.bank_id WHEN 3 THEN '0200' ELSE '0000' END AS bank_id" \
          " FROM" \
          "	sibu_directsale_profit_{db_index}.member_deal d" \
          " LEFT JOIN sibu_directsale_member_{db_index}.member_account c ON d.apply_member_id = c.member_id" \
          " LEFT JOIN sibu_directsale.member m ON m.member_id = d.apply_member_id" \
          " WHERE" \
          " d.apply_date >= '{start_date}' AND d.apply_date <= '{end_date}'"
    deals = list()
    for i in range(db_constants.DB_SIZE):
        module = StrUtil.format(i)
        db_url = DbUtil.get_db_url(module)
        db = pymysql.connect(host=db_url, user="root", passwd="Aa123456", db="sibu_directsale", charset="utf8mb4")
        cursor = db.cursor()
        result = cursor.execute(sql.format(db_index=module,start_date=start_date,end_date=end_date))
        if result is not 0:
            deals.extend(list(cursor.fetchall()))
        db.close()
        print_deal(deals)
def print_deal(deals):
    count = 0
    for i in deals:
        '''序号
        币种
        金额
        收款人账号
        收款人名称
        收款账号开户行名称
        收款省份 / 收款银行
        收款地市
        地区代码
        付款账号开户行名称
        付款人账号 / 卡号
        付款人名称 / 卡名称
        汇款用途
        备注
        预约付款日期
        汇款方式
        收款账户短信通知手机号码
        自定义序号
        协议编号
        '''
        count += 1
        print("%d,人民币" % (count,))
query_member_deal("2016-08-01 00:00:00", "2016-09-17 23:59:59")



