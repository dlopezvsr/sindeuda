from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


@app.post("/")
def post():
    return {"message": "hello world from the post rout"}