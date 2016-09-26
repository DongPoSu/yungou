from sevice import excel


# 银行卡提现
# excel.export_bank_deal("2016-09-23 00:00:00", "2016-09-26 23:59:59", "20160926")
# 微信提现
# excel.export_wx_deal("2016-09-23 00:00:00", "2016-09-23 23:59:59", "20160923")

excel.import_bank_deal("resources/5.27-5.29银行付款处理成功.xlsx")