from turtle import title
from urllib import response
from fastapi import Depends, FastAPI, status, Response, HTTPException
from . import  models, schemas
from .database import engine,SessionLocal
from typing import List, Union, Optional
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog',status_code=status.HTTP_201_CREATED)
async def create(request:schemas.BlogBase, db:Session=Depends(get_db)):

    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blog',response_model=List[schemas.ShowBlog])
async def all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog)
async def all_blogs(id,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with {id} id not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'blog with {id} id not found'} 
    return blog    


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id,request:schemas.BlogBase, db:Session=Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail=f'Cannot found blog {id}')
    blog.update({'title':request.title,'body':request.body})
    db.commit()
    return {'Updated'}


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id:int,db:Session=Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail=f'Cannot found blog {id}')
        

    blog.delete(synchronize_session=False)
    db.commit()

    
    return f'Blog deleted'