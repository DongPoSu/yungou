# coding=utf8

from sqlalchemy import Column, String
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class BillDeal(Base):
    __tablename__ = 'member'
    deal_code = Column(String, primary_key=True)
    apply_member_id = Column(String, primary_key=True)
    apply_date = Column(DateTime)
    apply_type = Column(Integer)
    deal_status = Column(String)
    apply_money = Column(Float)
    bank_account = Column(String)
    bankcard_address = Column(String)
    bank_user = Column(String)
    bankcard_province = Column(String)
    bankcard_city = Column(String)
    bankcard_area = Column(String)
    bank_id = Column(String)
    phone = Column(String)
    user_name = Column(String)
    give_invoice = Column(String)
    check_date = Column(DateTime)
    give_date = Column(DateTime)


# 定义User对象:
class BillDealResult(Base):
    __tablename__ = 'billdealresult'
    member_id = Column(String, primary_key=True)
    deal_id= Column(String, primary_key=True)
    apply_money = Column(Integer)
    give_invoice = Column(String)
    bank_account = Column(String)
    bank_user = Column(String)
    deal_status = Column(Integer)


