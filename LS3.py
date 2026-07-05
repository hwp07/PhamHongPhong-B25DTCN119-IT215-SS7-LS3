"""
phân tích:
- input: id, quantity
- output: thông báo thành công (201), thông báo lỗi/ thất bại: (404/400)
- các bước xử lý:
    + nhận request
    + kiểm tra sản phẩm có tồn tại hay không
    + kiểm tra số lượng có phù hợp hay không
    + trừ số lượng tồn kho
    + tạo đơn hàng và thêm và order_db
    + raise thông báo thành công
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2, "price": 600000.0}
]
orders_db = []

class OrderCreate(BaseModel):
    id: int
    stock: int

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    product = next(
        (p for p in products_db if p["id"] == order.id),
        None
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sản phẩm"
        )
    
    if order.stock <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0"
        )

    if order.stock > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )
    
    product["stock"] -= order.stock

    new_order = {
        "id": len(orders_db) + 1,
        "product_id": product["id"],
        "product_name": product["name"],
        "stock": order.stock,
        "total": order.stock * product["price"]
    }

    orders_db.append(new_order)

    return {
        "message": "Tạo đơn hàng thành công",
        "data": new_order
    }