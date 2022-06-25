from fastapi import Depends, FastAPI, status, Response, HTTPException,APIRouter
from typing import List, Union, Optional
from sqlalchemy.orm import Session
from blog import schemas, models
from blog.database import get_db
from blog.hashing import Hash

router = APIRouter()


# <---------------User API--------------->
@router.post('/user',response_model=schemas.ShowUser,tags=['user'])
async def create_user(request:schemas.User,db:Session=Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get('/users',response_model=List[schemas.ShowUser],tags=['user'])
async def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users



@router.get('/users/{id}',response_model=schemas.ShowUser,tags=['user'])
async def get_users(id,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with {id} id not found')
    return user



@router.delete('/users/{id}',tags=['user'])
async def delete_user(id,db:Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with {id} id not found')

    user.delete(synchronize_session=False)
    db.commit()
    return f'User deleted'



