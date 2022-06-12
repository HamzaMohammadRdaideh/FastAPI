from typing import List, Union, Optional
from fastapi import FastAPI
from models import *

app = FastAPI()

# db : List[User] = [

#     User(
#         id=UUID("3bc14b06-4088-423a-ab8b-7704d6014eae"),
#         first_name = 'Ahmad',
#         middle_name = 'Mohammad',
#         last_name = 'Samer',
#         gender = Gender.male,
#         roles= [Role.admin]
#     ),

#     User(
#         id=UUID("7a41fcbb-4495-4efb-9e57-7c1ccd2ee757"),
#         first_name = 'Rami',
#         middle_name = 'Issa',
#         last_name = 'Amr',
#         gender = Gender.male,
#         roles = [Role.stundent]
#     ),
#     User(
#         id=UUID("ef212217-12da-4de7-94d5-59f6962bf324"), 
#         first_name = 'sara',
#         middle_name = 'sara',
#         last_name = 'sara',
#         gender = Gender.female,
#         roles = [Role.user]
#     )    

# ] 
 

@app.get('/blog')
async def read_root(limit = 10, published : bool = True, sort : Optional[str] = None):
    # only 10 published blogs

    if published:
        return {'data': f' {limit} published Blogs from db'}
    else:
        return {'data': f' {limit} Blogs from db'}    


@app.get('/blog/unpublished')
async def unpublished_blogs():

    return {'data':'unpublished blogs'}


@app.get('/blog/{id}')
async def fetch_blog(id:int):
    
    # fetch blog with id = id

    return{'data' : id};   


@app.get('/blog/{id}/comments')
async def comments(id, limit = 10):

    # fetch comments of blog
    return {'data' : {'comments':'com1'}};


@app.post('/blog')
async def create_blog(blog:Blog):

    return f'Blog created and save as {blog.title}'




    