from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Usuários"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def criar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    novo_user = User(
        nome=user.nome,
        email=user.email,
        senha=user.senha
    )
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user
