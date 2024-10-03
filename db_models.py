from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Double
from sqlalchemy.orm import relationship
from database import Base
import uuid
import os

class Coupon(Base):
    __tablename__ = "coupon"
    id = Column(String(256),primary_key=True)
    code = Column(String(256))
    id_type = Column(String(256))

class CouponDetails(Base):
    __tablename__ = "coupon_details"
    id_coupon = Column(String(256),primary_key=True)
    percentage = Column(Integer)
    id_user = Column(String(256))
    quantity = Column(Integer)

class CouponRedeem(Base):
    __tablename__ = "coupon_reedem"
    id_operation = Column(String(256),primary_key=True, default=uuid.uuid4)
    id_user = Column(String(256))
    id_coupon = Column(String(256))

class CouponType(Base):
    __tablename__ = "coupon_type"
    id = Column(String(256),primary_key=True)
    description = Column(String(256))
    type = Column(String(256))

class Product(Base):
    __tablename__ = "products"
    id = Column(String(256),primary_key=True)
    description = Column(String(256))
    id_category = Column(String(256))
    price = Column(Double)
    image_url = Column(String(256))

class CouponSettings(Base):
    __tablename__ = "coupon_settings"
    id = Column(String(256),primary_key=True)
    field = Column(String(256))
    value = Column(String(256))