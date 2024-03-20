from fastapi import FastAPI, HTTPException
from src.application.api_data_models import UserSchema
from src.services import user_service

app = FastAPI()


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


@app.post("/transactions/{user_id}")
async def add_transaction(user_id: str):
    return {"message": "hello world from the post route"}
