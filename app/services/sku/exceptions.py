from fastapi import HTTPException


class SkuNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Sku not found")


class SkuAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Sku with provided id already exists",
        )
