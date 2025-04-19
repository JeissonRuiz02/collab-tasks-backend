from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from .jwt import create_access_token
from ..models.user import UserCreate
from ..services.firestore import get_user_by_email, create_user
from ..auth.security import pwd_context

router = APIRouter(prefix="/auth", tags=["Auth"])

fake_user = {
    "email": "admin@test.com",
    "hashed_password": pwd_context.hash("admin123")
}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
def register_user(user: UserCreate):
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    return create_user(user)