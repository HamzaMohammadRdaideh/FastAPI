import email
from turtle import title
from unicodedata import name
from urllib import response
import bcrypt
from fastapi import Depends, FastAPI, status, Response, HTTPException
from . import  models, schemas
from .database import engine,SessionLocal
from typing import List, Union, Optional
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# <---------------User API--------------->
@app.post('/user',response_model=schemas.ShowUser,tags=['user'])
async def create_user(request:schemas.User,db:Session=Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# <---------------Blog API--------------->
@app.post('/blog',status_code=status.HTTP_201_CREATED,tags=['blog'])
async def create(request:schemas.BlogBase, db:Session=Depends(get_db)):

    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blog',response_model=List[schemas.ShowBlog],tags=['blog'])
async def all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBlog,tags=['blog'])
async def all_blogs(id,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'blog with {id} id not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail':f'blog with {id} id not found'} 
    return blog    


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['blog'])
async def update_blog(id,request:schemas.BlogBase, db:Session=Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail=f'Cannot found blog {id}')
    blog.update({'title':request.title,'body':request.body})
    db.commit()
    return {'Updated'}


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['blog'])
async def delete_blog(id:int,db:Session=Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status=status.HTTP_404_NOT_FOUND,detail=f'Cannot found blog {id}')
        

    blog.delete(synchronize_session=False)
    db.commit()

    
    return f'Blog deleted'