from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends
from src.application.api_data_models import UserSchema
from fastapi.security import OAuth2PasswordBearer
from src.services import user_service

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/register")
async def register_user(user_shema: UserSchema):
    if user_service.user_validation(user_shema.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_service.add_user_service(
        user_shema.name,
        user_shema.lastname,
        user_shema.email,
        user_shema.password
    )
    return {"message": "User created succesfully"}


@app.post("/login")
async def register_user(user_email: str, user_password: str):
    user = user_service.user_validation(user_email)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if user_service.authenticate_user(user_email, user_password):
        access_token = user_service.create_access_token(
            data={"sub": user.email}
        )
        return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = User(username=username)
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return UserInDB(**user)


@app.post("/transactions/{user_id}")
async def add_transaction(current_user=Depends(get_current_user)):
    return current_user
