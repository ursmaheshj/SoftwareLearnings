from pydantic import BaseModel

class CreateUSer(BaseModel):
    name: str
    email: str

class OutUser(CreateUSer):
    id: int

class UpdateUser(BaseModel):
    name: str | None = None
    email: str | None = None



