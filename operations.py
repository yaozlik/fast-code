from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from database import engine
import uuid
from db_models import Coupon, CouponDetails, CouponRedeem, CouponType, CouponSettings
from models import ApplyCoupon

def get_coupon_by_code(code: str, db: Session):
    return db.query(Coupon).filter(Coupon.code == code).first()

def get_details_by_coupon_id(id: str, db: Session):
    return db.query(CouponDetails).filter(CouponDetails.id_coupon == id).first()

def get_type_by_id(id: str, db: Session):
    return db.query(CouponType).filter(CouponType.id == id).first()

def get_sum_products(ids: List[str]):
    statement = text("""SELECT SUM(price) AS total FROM product where id in :values ;""")
    query = statement.bindparams(values=tuple(ids))
    conn = engine.connect()
    rs = conn.execute(query).fetchone()
    return rs[0]

def get_coupon_book(coupon_id):
    statement = text("""SELECT count(*) AS total FROM coupon_reedem where id_coupon = :values ;""")
    query = statement.bindparams(values=coupon_id)
    conn = engine.connect()
    rs = conn.execute(query).fetchone()
    return rs[0]

def get_coupon_setting_value_by_field(field: str, db:Session):
    return db.query(CouponSettings).filter(CouponSettings.field == field).first()

def create_transaction(id_user: str, id_coupon, db: Session):
    transaction = CouponRedeem(id_user=id_user, id_coupon=id_coupon)
    db.add(transaction)
    db.commit()
    db.flush()

def create_transaction_no_coupon(id_user: str, db: Session):
    transaction = CouponRedeem(id_user=id_user)
    db.add(transaction)
    db.commit()
    db.flush()

def create_gift_card_unique(id_user: str, db:Session, percentage: int, code:str, type:str):
    id = f'{uuid.uuid4()}'
    gift_card = Coupon(id = id, code=code, id_type=type)
    db.add(gift_card)
    details = CouponDetails(id_coupon=id, percentage=percentage, quantity=1, id_user=id_user)
    db.add(details)
    db.commit()
    db.flush()


def get_id_by_type(type:str, db: Session):
    return db.query(CouponType).filter(CouponType.type == type).first()