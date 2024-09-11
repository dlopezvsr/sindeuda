import json

from fastapi.responses import JSONResponse

from src.models.api_data_models import (UserSchema, UserLoginSchema,
                                        AccountSchema, CategorySchema,
                                        TransactionPromptSchema)
from src.use_cases import openai_use_case
from src.services import user_service, account_service, category_service
from fastapi import FastAPI, HTTPException, Depends, status, Response
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
    "http://localhost:3032"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/auth/sign-up")
async def register_user(user_schema: UserSchema) -> dict:
    user = await user_service.get_user_service(user_schema.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    await user_service.add_user_service(user_schema)
    return {"message": "User created successfully"}


@app.post("/api/auth/sign-in")
async def login_user(user_login_form: UserLoginSchema) -> dict:
    user = await user_service.get_user_service(user_login_form.email)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")
    user_auth = await user_service.authenticate_user(user_login_form.email, user_login_form.password)
    if user_auth:
        data = {"sub": str(user.id)}
        access_token = user_service.create_access_token(data)
        response_data = {
            "user": {
                "id": str(user.id),
                "email": user.email
            },
            "accessToken": access_token
        }
        return JSONResponse(content=response_data, status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Your password is incorrect.")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, os.environ.get("SECRET_KEY"),
            algorithms=[os.environ.get('ALGORITHM')]
        )
        user_id: str = payload["sub"]

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_service.user_id_validation(user_id)
    if user.id is None:
        raise credentials_exception
    return user


@app.get("/api/auth/me", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_user)):
    print(current_user)
    return {
        "id": str(current_user.id),  # Ensure UUID is converted to string
        "email": current_user.email,
    }


@app.post("/accounts/add/account")
async def add_account(account: AccountSchema, token=Depends(get_current_user)):
    if account_service.get_account_service(account.card_name, account.user_id):
        raise HTTPException(status_code=400, detail="Account alredy exists")

    await account_service.add_account_service(account)
    return account


@app.post("/categories/add/category")
async def add_category(category: CategorySchema, token=Depends(get_current_user)):
    if category_service.get_category_service(category.category_name, category.user_id):
        raise HTTPException(status_code=400, detail="Category already exists")

    await category_service.add_category_service(category)
    return category


@app.get("/categories/get/categories/{user_id}")
async def get_all_categories(user_id, token=Depends(get_current_user)):
    # TODO: Develop error handling
    # raise HTTPException(status_code=400, detail="Category already exists")

    db_categories = await category_service.get_all_categories_service(user_id)
    response = [{"category_name": tuple(row)[1],
                 "type": tuple(row)[2],
                 "expense_budget": tuple(row)[3]} for row in db_categories]
    response = {
        "status_code": status.HTTP_200_OK,
        "categories": response,
    }
    return Response(content=json.dumps(response), media_type="application/json")


@app.post("/transactions/query/transaction")
async def query_transaction(prompt_text: TransactionPromptSchema, token=Depends(get_current_user)):
    response = openai_use_case.prompt_processor(prompt_text.prompt_text, prompt_text.user_id)
    return Response(content=response, media_type="text/plain")
