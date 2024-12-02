# app/routers/user_info.py

from fastapi import APIRouter, HTTPException, Request
from app.models import Link, UserInfo, UsernameChangeRequest
from app.resources.user_info_resource import UserInfoResource

router = APIRouter()
user_info_resource = UserInfoResource()

@router.get('/user_info/{username}/{password}', response_model=UserInfo)
def login(username: str, password: str, request: Request):
    user = user_info_resource.get_by_key(username)
    if not user or not password == user.password:
        raise HTTPException(status_code=401,
                            detail='Invalid username or password')
    user.links = [Link(rel='self', href=str(request.url))]
    return user

@router.post('/user_info/')
def signup(user_info: UserInfo):
    if user_info_resource.get_by_key(user_info.username):
        raise HTTPException(status_code=400, detail='User already exists')
    user_info_resource.create(user_info)
    return {'message': 'User signed up'}

@router.put('/user_info/')
def change_name(name_change: UsernameChangeRequest):
    user = user_info_resource.get_by_key(name_change.old_username)
    if (not user or name_change.password != user.password or
        user_info_resource.get_by_key(name_change.new_username)):
        raise HTTPException(status_code=401,
                            detail='Invalid username or password')
    user.username = name_change.new_username
    user_info_resource.update(name_change.old_username, user)
    return {'message': 'Username changed successfully'}

@router.delete('/user_info/')
def delete(user_info: UserInfo):
    user = user_info_resource.get_by_key(user_info.username)
    if (not user or user_info.password != user.password):
        raise HTTPException(status_code=401,
                            detail='Invalid username or password')
    user_info_resource.delete(user_info.username)
    return {'message': 'User deleted successfully'}
