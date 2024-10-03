from pydantic import BaseModel, validator
from typing import List, Optional

class ApplyCoupon(BaseModel):
    coupon: str
    user: str
    products: List[str]


class PayModel(BaseModel):
    coupon: Optional[str] = None
    user: str
    products: List[str]