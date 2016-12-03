# coding=utf8

from sqlalchemy import Column, String
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class DoingOrder(Base):
    __tablename__ = 'doing_order'
    order_id = Column(String, primary_key=True)
    member_id = Column(String)
    order_code = Column(String)
    phone = Column(String)


# 定义User对象:
class TransferRecord(Base):
    __tablename__ = 'transfer_record'
    transfer_id = Column(String, primary_key=True)
    transfer_code = Column(String, primary_key=True)
    transfer_money = Column(Float)
    out_user_name = Column(String)
    out_phone = Column(String)
    in_user_name = Column(String)
    in_phone = Column(String)
    transfer_memo = Column(String)
    create_time = Column(DateTime)
