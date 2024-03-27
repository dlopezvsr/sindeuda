from typing import Annotated
from fastapi import FastAPI, HTTPException, Depends, status
from src.application.api_data_models import UserSchema, UserLoginSchema, AccountSchema, CategorySchema
from fastapi.security import OAuth2PasswordBearer
from src.services import user_service, account_service
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/register")
async def register_user(user_shema: UserSchema):
    if user_service.get_user_service(user_shema.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_service.add_user_service(user_shema)
    return {"message": "User created succesfully"}


@app.post("/login")
async def register_user(user_login_form: UserLoginSchema):
    user = user_service.get_user_service(user_login_form.email)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if user_service.authenticate_user(user_login_form.email, user_login_form.password):
        data = {"sub": user.id}
        access_token = user_service.create_access_token(data)
        return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms=[os.environ.get('ALGORITHM')])
        user_id: str = payload["sub"]

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.user_id_validation(user_id)
    if user.id is None:
        raise credentials_exception
    return user_id


@app.post("/accounts/add/account")
async def add_account(account: AccountSchema, token=Depends(get_current_user)):
    return account


@app.post("/categories/add/category")
async def add_category(category: CategorySchema, token=Depends(get_current_user)):
    return category


@app.post("/transactions/query/transaction")
async def query_transaction(token=Depends(get_current_user)):
    # TODO: 1. Handle string query, recive it correctly from body sent by user.
    # TODO: 2. Pass string to Lanchain function that will return a dict.
    # TODO: 3. Retrieve dict from previous function and post to DB using Transaction Model
    pass
