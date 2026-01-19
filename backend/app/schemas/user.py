from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UserUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = None
