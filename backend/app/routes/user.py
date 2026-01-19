from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
router = APIRouter(prefix="/users", tags=["Usuários"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def criar_usuario(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se email já existe
    existe = db.query(User).filter(User.email == user.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo_user = User(
        nome=user.nome,
        email=user.email,
        senha=user.senha
    )
    db.add(novo_user)
    db.commit()
    db.refresh(novo_user)
    return novo_user


@router.get("/")
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(User).all()
    return [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "senha": u.senha
        }
        for u in usuarios
    ]


@router.get("/{user_id}")
def buscar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": usuario.senha
    }


@router.delete("/{user_id}")
def deletar_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}


@router.put("/{user_id}")
def atualizar_usuario(user_id: int, dados: UserUpdate, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.id == user_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if dados.nome is not None:
        usuario.nome = dados.nome

    if dados.email is not None:
        existe = db.query(User).filter(User.email == dados.email, User.id != user_id).first()
        if existe:
            raise HTTPException(status_code=400, detail="Email já cadastrado por outro usuário")
        usuario.email = dados.email

    if dados.senha is not None:
        usuario.senha = dados.senha

    db.commit()
    db.refresh(usuario)

    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": usuario.senha
    }
