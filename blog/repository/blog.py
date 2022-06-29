from fastapi import APIRouter
from fastapi import Depends, FastAPI, status, Response, HTTPException
from typing import List, Union, Optional
from sqlalchemy.orm import Session
from blog.database import get_db
from .. import models, schemas


def get_all_blogs(db:Session):

    blogs = db.query(models.Blog).all()
    return blogs


def create_blog(request:schemas.Blog,db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def get_blog(id:int,db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with {id} id not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'blog with {id} id not found'}
    return blog