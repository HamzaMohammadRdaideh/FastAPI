from typing import Optional
from click import UUID
from pydantic import BaseModel
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional,List

# class Gender(str,Enum):
#     male = "male"
#     female = "female"


# class Role(str,Enum):
#     admin = "admin"
#     stundent = "stundent"
#     user = "user"


# class User(BaseModel):
#     id : Optional[UUID] = uuid4()
#     first_name : str
#     middle_name : Optional[str]
#     last_name : str
#     gender : Gender
#     roles : List[Role]

class Blog(BaseModel):
    
    title : str
    body : str
    published : Optional[bool]