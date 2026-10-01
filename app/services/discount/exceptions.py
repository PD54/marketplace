from fastapi import HTTPException


class DiscountNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Discount not found",
        )
