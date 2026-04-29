from fastapi import HTTPException


class BadRequest(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="No id provided")


class NotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Not found")
