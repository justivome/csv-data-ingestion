from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.auth import create_access_token, hash_password, verify_password
from app.deps import CurrentUserDep, SessionDep
from app.models.user import User
from app.schemas.auth import Token, UserLogin, UserRead, UserRegister

router = APIRouter()


@router.post("/register", response_model=Token)
def register(body: UserRegister, session: SessionDep):
    existing = session.exec(select(User).where(User.email == body.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )

    user = User(
        name=body.name,
        email=body.email,
        hashed_password=hash_password(body.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(body: UserLogin, session: SessionDep):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUserDep):
    return current_user
