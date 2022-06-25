import email
from turtle import title
from unicodedata import name
from urllib import response
import bcrypt
from fastapi import Depends, FastAPI, status, Response, HTTPException
from . import  models, schemas
from .database import engine, SessionLocal, get_db
from typing import List, Union, Optional
from sqlalchemy.orm import Session
from .hashing import Hash
from blog.routers import blog, user

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)


