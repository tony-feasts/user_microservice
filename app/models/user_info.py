# app/models/user_info.py

from pydantic import BaseModel
from typing import List
from app.models.link import Link

class UserInfo(BaseModel):
    username: str
    password: str
    links: List[Link] = None
