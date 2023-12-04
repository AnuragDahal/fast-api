# in fast api we call pydantic model as schemas and sql alchemy model as model
from pydantic import BaseModel


class Blog(BaseModel):#
    title:str   
    body:str
    
    
class show(Blog): 
    title:str
    body:str

    
    
# class User(Blog):
#     name:str
#     email:str
#     password:str
    