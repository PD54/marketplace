from uuid import UUID

from pydantic import BaseModel


class getItemInfoResponse(BaseModel):
    id: UUID
    sku_id: UUID
    stock: str
    reserved_state: bool