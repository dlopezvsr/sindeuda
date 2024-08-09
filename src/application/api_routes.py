from src.models.api_data_models import UserSchema, UserLoginSchema, AccountSchema, CategorySchema, TransactionSchema
from src.services import user_service, account_service, category_service
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def register_user(user_shema: UserSchema) -> dict:
    if user_service.get_user_service(user_shema.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_service.add_user_service(user_shema)
    return {"message": "User created succesfully"}


@app.post("/login")
async def login_user(user_login_form: UserLoginSchema) -> dict:
    user = user_service.get_user_service(user_login_form.email)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    if user_service.authenticate_user(user_login_form.email, user_login_form.password):
        data = {"sub": str(user.id)}
        access_token = user_service.create_access_token(data)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Your password is incorrect.")


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
    if account_service.get_account_service(account.card_name, account.user_id):
        raise HTTPException(status_code=400, detail="Account alredy exists")

    account_service.add_account_servcie(account)
    return account


@app.post("/categories/add/category")
async def add_category(category: CategorySchema, token=Depends(get_current_user)):
    if category_service.get_category_service(category.category_name, category.user_id):
        raise HTTPException(status_code=400, detail="Category already exists")

    category_service.add_category_service(category)
    return category


@app.post("/transactions/query/transaction")
async def query_transaction(prompt_text: TransactionSchema, token=Depends(get_current_user)):
    # TODO: 1. Handle string query, receive it correctly from body sent by user.
    # TODO: 2. Pass string to Langchain function that will return a dict.
    # TODO: 3. Retrieve dict from previous function and post to DB using Transaction Model
    pass
