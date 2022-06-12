from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str

class ShowBlog(BlogBase):
    class Config:
        orm_mode = True


# class ShowBlog(BlogBase):
#     title:str
#     class Config:
#         orm_mode = True        