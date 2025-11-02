from pydantic import BaseModel

class Transaction(BaseModel):
    time_ind: int
    transac_type: str
    amount: float
    src_acc: str
    dst_acc: str
    src_bal: float
    src_new_bal: float
    dst_bal: float
    dst_new_bal: float
    is_flagged_fraud: int