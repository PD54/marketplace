from fastapi import HTTPException


class GoodNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Good not found")
