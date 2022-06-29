from fastapi import APIRouter
from fastapi import Depends, FastAPI, status, Response, HTTPException
from typing import List, Union, Optional
from sqlalchemy.orm import Session

import blog.repository.blog
from blog import schemas, models
from blog.database import get_db
from blog.repository import *

router = APIRouter(
    tags=['blog'],
    prefix='/blog'
)


# <---------------Blog API--------------->
@router.post('/', response_model=schemas.ShowBlog, status_code=status.HTTP_201_CREATED)
async def create(request: schemas.BlogBase, db: Session = Depends(get_db)):
    return blog.create_blog(request,db)

@router.get('/', response_model=List[schemas.ShowBlog])
async def all_blogs(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def all_blogs(id, response: Response, db: Session = Depends(get_db)):
    return blog.get_blog(id,db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail=f'Cannot found blog {id}')
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return {'Updated'}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail=f'Cannot found blog {id}')

    blog.delete(synchronize_session=False)
    db.commit()

    return f'Blog deleted'