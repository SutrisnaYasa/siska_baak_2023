from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import date
import re

# Membuat pilihan untuk role user dengan Enum
class Roles(str, Enum):
    user = "user",
    admin = "admin"

# Schemas User
class User(BaseModel):
    username: str
    password: str
    role: Roles
    status: bool = True

class ShowUser(BaseModel):
    username: str
    status : bool = True
    role: Roles

    class Config():
        orm_mode = True

# End Schemas User

# Schemas Login
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# End Schemas Login
