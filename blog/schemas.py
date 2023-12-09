# in fast api we call pydantic model as schemas and sql alchemy model as model
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class show(Blog):
    title: str
    body: str

    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    password: str

    class Config():
        from_attributes = True  # orm_mode has been renamed to from_attributes
