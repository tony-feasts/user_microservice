# app/models/link.py

from pydantic import BaseModel

class Link(BaseModel):
    rel: str
    href: str
