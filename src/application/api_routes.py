from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from src.application.api_data_models import UserSchema, UserLoginSchema
from fastapi.security import OAuth2PasswordBearer
from src.services import user_service
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

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
async def register_user(user_login_form: UserLoginSchema):
    user = user_service.user_validation(user_login_form.email)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if user_service.authenticate_user(user_login_form.email, user_login_form.password):
        data = {"sub": user.email}
        access_token = user_service.create_access_token(data)
        return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get('ALGORITHM')])
        username: str = payload["sub"]

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.user_validation(username)
    if user.email is None:
        raise credentials_exception
    return user


@app.get("/transactions/user_id")
async def add_transaction(user_id=Depends(get_current_user)):
    return user_id.email
