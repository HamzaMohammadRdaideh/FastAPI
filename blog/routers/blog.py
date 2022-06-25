from fastapi import APIRouter
from fastapi import Depends, FastAPI, status, Response, HTTPException
from typing import List, Union, Optional
from sqlalchemy.orm import Session
from blog import schemas, models
from blog.database import get_db

router = APIRouter()


# <---------------Blog API--------------->
@router.post('/blog', response_model=schemas.ShowBlog, status_code=status.HTTP_201_CREATED, tags=['blog'])
async def create(request: schemas.BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['blog'])
async def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blog'])
async def all_blogs(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with {id} id not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'blog with {id} id not found'}
    return blog


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
async def update_blog(id, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail=f'Cannot found blog {id}')
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return {'Updated'}


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
async def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail=f'Cannot found blog {id}')

    blog.delete(synchronize_session=False)
    db.commit()

    return f'Blog deleted'