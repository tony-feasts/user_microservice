# app/models/user_info.py

from pydantic import BaseModel
from typing import List
from app.models.link import Link

class UserInfo(BaseModel):
    username: str
    # google_sub is basically a unique identifier from Google OAuth
    google_sub: str
    links: List[Link] = None
