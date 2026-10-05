from fastapi import HTTPException


class TaskNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="TaskNotFound",
        )
