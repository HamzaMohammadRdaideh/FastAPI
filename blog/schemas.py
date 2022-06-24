from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str

class ShowBlog(BlogBase):
    title: str
    body: str
    class Config:
        orm_mode = True


# class ShowBlog(BlogBase):
#     title:str
#     class Config:
#         orm_mode = True        



class User(BaseModel):
    name: str
    email: str 
    password:str


class ShowUser(BaseModel):
    name: str
    email: str 

    class Config:
        orm_mode = True
   