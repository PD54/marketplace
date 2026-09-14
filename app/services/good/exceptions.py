from fastapi import HTTPException


class GoodNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Good not found")


class GoodAlreadyOnNotFoundStockError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Good is already on not_found stock",
        )
