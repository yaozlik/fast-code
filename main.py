from fastapi import FastAPI, Depends, HTTPException
from models import ApplyCoupon, PayModel
from typing import List
from operations import get_coupon_by_code, get_details_by_coupon_id, get_type_by_id, get_sum_products, get_coupon_book, create_transaction_no_coupon, create_gift_card_unique, get_id_by_type, create_transaction, get_coupon_setting_value_by_field
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import time    


app = FastAPI()

def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Welcome to Fast Coupon by Osmi"}


@app.post("/applycoupon")
async def applycoupon(data: ApplyCoupon, db:Session=Depends(get_db)):
    ## Find coupon data
    code = data.coupon
    coupon_db = get_coupon_by_code(code=code, db=db)
    
    total = 0
    ## IF not exist coupon return error
    if (coupon_db is None):
        return {"status": "COUPON_NOT_FOUND", "message": "Coupon doesn't exist"}
    
    print("My ID coupon")
    print(coupon_db.id)

    #
    ## Get Coupon Details
    coupon_details_db = get_details_by_coupon_id(id=coupon_db.id, db=db)

    # Validate coupon book
    coupon_available = validate_coupon_book(coupon_db.id, coupon_details_db.quantity)
    print("Coupon Available")
    print(coupon_available)
    if not coupon_available:
        return {"status": "COUPON_REACH_LIMIT", "message": "Coupon reach limit"}
    ## Get Coupon Type    
    coupon_type_db = get_type_by_id(id=coupon_db.id_type, db=db)
    print("Coupon Type")
    print(coupon_type_db.type)
    coupon_type = coupon_type_db.type

    ## Find products and sum prices
    subtotal = get_sum_products(data.products)
    print("Total products price")
    print(subtotal)
    discount = 0
    ## I have only 2 types for now: Gift card (unique by user), and Percentage Discount 
    ## Apply Coupon discount (or any logic)
    if (coupon_type == "COUPON_PERCENTAGE"):
        print("Logic to discount %")
        percentage = int(coupon_details_db.percentage)
        discount = (subtotal * percentage) / 100
        total = subtotal - (subtotal * percentage / 100)
        print("------Total----")
        print(total)
    if (coupon_type == "GIFT_CARD"): 
        print("Logic to discount % wit GIFT CARD")
        ## Validate if coupon is own by user
        if (coupon_details_db.id_user == data.user):
            percentage = int(coupon_details_db.percentage)
            discount = (subtotal * percentage) / 100
            total = subtotal - (subtotal * percentage / 100)
            print("------Total----")
            print(total)
        else:
            return {"status": "COUPON_NOT_FOUND", "message": "coupon doesn't belong to the user"}

    resultdata = {"coupon": data.coupon, "subtotal": subtotal, "total": total, "discount": discount}
    return {"status": "COUPON_APPLIED", "message": "Coupon was applied", "data": resultdata} 


@app.post("/pay")
async def pay(data: PayModel, db:Session=Depends(get_db)):
     ## Find coupon data
    code = data.coupon
    coupon_db = get_coupon_by_code(code=code, db=db)
   
    ## Find products and sum prices
    subtotal = get_sum_products(data.products)
    print("Total products price")
    print(subtotal)
    discount = 0

    ## If not coupon given
    if (data.coupon is None):
        complete_transaction(id_coupon=data.coupon, id_user=data.user, db=db)
        generate_gift_card(data.user, db=db)
        resultdata = {"subtotal": subtotal, "total": subtotal, "discount": discount}
        return {"status": "PAY_SUCCESS", "message": "pay was success", "data": resultdata} 
        
    ## IF not exist coupon return error
    if (coupon_db is None):
        resultdata = {"subtotal": subtotal, "total": subtotal, "discount": discount}
        return {"status": "COUPON_NOT_FOUND", "message": "Coupon doesn't exist", "data": resultdata}
    
    print("My ID coupon")
    print(coupon_db.id)

    ## Get Coupon Details
    coupon_details_db = get_details_by_coupon_id(id=coupon_db.id, db=db)
    print("Coupon ID........")
    print(coupon_db.id)
    # Validate coupon book
    coupon_available = validate_coupon_book(coupon_db.id, coupon_details_db.quantity)
    print("Coupon Available")
    print(coupon_available)
    if not coupon_available:
        resultdata = {"subtotal": subtotal, "total": subtotal, "discount": discount}
        return {"status": "COUPON_REACH_LIMIT", "message": "Coupon reach limit", "data": resultdata}
    ## Get Coupon Type    
    coupon_type_db = get_type_by_id(id=coupon_db.id_type, db=db)
    print("Coupon Type")
    print(coupon_type_db.type)
    coupon_type = coupon_type_db.type
    total = 0
    
    ## I have only 2 types for now: Gift card (unique by user), and Percentage Discount 
    ## Apply Coupon discount (or any logic)
    if (coupon_type == "COUPON_PERCENTAGE"):
        print("Logic to discount %")
        percentage = int(coupon_details_db.percentage)
        discount = (subtotal * percentage) / 100
        total = subtotal - (subtotal * percentage / 100)
        print("------Total----")
        print(total)
    if (coupon_type == "GIFT_CARD"): 
        print("Logic to discount % wit GIFT CARD")
        ## Validate if coupon is own by user
        if (coupon_details_db.id_user == data.user):
            percentage = int(coupon_details_db.percentage)
            discount = (subtotal * percentage) / 100
            total = subtotal - (subtotal * percentage / 100)
            print("------Total----")
            print(total)
        else:
            resultdata = {"subtotal": subtotal, "total": subtotal, "discount": discount}
            return {"status": "COUPON_NOT_FOUND", "message": "coupon doesn't belong to the user", "data":resultdata}

    
    ## Create transaction (In my opinion we need create a table for transactions, but I omitted and I created only coupon_reedem)
    complete_transaction(id_coupon=coupon_db.id, id_user=data.user, db=db)

    generate_gift_card(data.user, db=db)

    resultdata = {"coupon": data.coupon, "subtotal": subtotal, "total": total, "discount": discount}
    return {"status": "COUPON_APPLIED", "message": "Coupon was applied", "data": resultdata} 

@app.get("/maxcoupons")
async def get_max_coupon_per_user(db:Session=Depends(get_db)):
    field = get_coupon_setting_value_by_field(field="MAX_PER_USER", db=db)
    resultdata = {"max_coupons": field.value}
    return {"status": "success", "data":resultdata}

def validate_coupon_book(coupon_id, quantity):
    book = get_coupon_book(coupon_id=coupon_id)
    print("---Boooooook---")
    print(book)
    if (book < quantity):
        return True
    return False

def generate_gift_card(id_user, db):
    print("generate_gift_card")
    ## Get id of GiftCard Value
    coupon_type = get_id_by_type(type="GIFT_CARD", db=db)
    id = coupon_type.id
    epoch_time = int(time.time())
    code = "wf" + str(epoch_time)
    ## We can get the percentage by settings GIFT_CARD_VALUE
    create_gift_card_unique(id_user=id_user,percentage=15, code=code, db=db, type=id)
    

def complete_transaction(id_user, id_coupon, db):
    if (id_coupon is None):
        create_transaction_no_coupon(id_user=id_user, db=db)
    else:
        create_transaction(id_coupon=id_coupon, id_user=id_user, db=db)