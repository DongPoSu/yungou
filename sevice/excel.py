# coding=utf8

import os

from openpyxl import Workbook
from openpyxl import load_workbook

from constants.db_constants import BILL_DEAL, NORMAL_DEAL
from sevice.member_deal import query_deal


# 导出发票提现打款
from sevice.order_service import update_order_trade


def export_bill_deal(check_start_date, check_end_date, title):
    '''
    :param check_start_date: 审核开始日期
    :param check_end_date:  审核结束日期
    :param title: 文件名
    :return:
    '''
    deals = query_deal(check_start_date, check_end_date, BILL_DEAL)
    wb = Workbook()
    ws = wb.active
    head_line = ['提现号','审核日期','序号', '币种', '金额', '收款人账号', '收款人名称', '收款账号开户行名称', '收款省份/收款银行',
                 '收款地市', '地区代码', '付款账号开户行名称', '付款人账号/卡号', '付款人名称 / 卡名称',
                 '汇款用途', '备注', '预约付款日期', '汇款方式', '收款账户短信通知手机号码', '自定义序号', '协议编号']
    ws.append(head_line)
    count = 0
    for deal in deals:
        count += 1
        ws.append(
            [deal.deal_code,deal.check_date.strftime('%Y-%m-%d %H:%M:%S'), count, "人民币", deal.apply_money, deal.bank_account, deal.bank_user, deal.bankcard_address,
             deal.bankcard_province,
             deal.bankcard_city, deal.bank_id, "工行广州花都雅居乐支行", "广州思埠网络开发有限公司", "3602202119100259501", "代付款","",
             title, "", deal.phone, "", ""])

    wb.save("resources/%s发票打款名单.xlsx" % (title))


# 导出提现结果
def export_deal(give_start_date, give_end_date, title):
    '''
    :param give_start_date: 打款开始时间
    :param give_end_date: 打款结束时间
    :param title:
    :return:
    '''
    deals = query_deal(give_start_date, give_end_date, NORMAL_DEAL)
    wb = Workbook()
    ws = wb.active
    head_line = ['序号', '姓名', '手机号', '提现金额', '提现状态', '申请日期', '打款备注', '打款日期']
    ws.append(head_line)
    count = 0
    for deal in deals:
        count += 1
        ws.append(
            [count, deal.user_name, deal.phone, deal.apply_money, deal.deal_status,
             deal.apply_date.strftime('%Y-%m-%d %H:%M:%S'), deal.give_invoice,
             deal.give_date.strftime('%Y-%m-%d %H:%M:%S')])
    wb.save("resources/%s提现打款结果.xlsx" % (title))


def import_order_trade_id(filename):
    wb = load_workbook(filename=filename, read_only=True)
    ws = wb['Sheet1']  # ws is now an IterableWorksheet
    list=[]
    for row in ws.rows:
        if str(row[0].value) == "":
            pass
        data = str(row[0].value),str(row[1].value)
        list.append(data)
    update_order_trade(list)
    # print(len(list))
# import_order_trade_id('resources/0804_0818_wechat_trade.xlsx')
