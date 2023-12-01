# Purpose: To define the schema for the blog post
from pydantic import BaseModel


class Blog(BaseModel):#
    title:str   
    body:str
    