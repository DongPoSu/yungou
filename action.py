

from sevice import excel


# 银行卡提现
# excel.export_bank_deal("2016-12-12 00:00:00", "2016-12-14 23:59:59", "201612015")
# 微信提现
excel.export_wx_deal("2016-12-14 00:00:00", "2016-12-14 23:59:59", "201612015")

# excel.import_bank_deal("resources/20160922银行卡打款结果.xlsx")

# 导出转账记录
# excel.export_transfer_records("截止20161104-1转账记录")




