from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import User
from Users.route import userRouter


def get_application():
    _app = FastAPI(title= "Auth Api", version="1.0.0")

    origins = [
        "*",
    ]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
        expose_headers=["X-Total-Pages"],  # Expose custom header to the client
    )

    return _app

app = get_application()

@app.get("/")
def home():
    return {"Hello": "World"}

app.include_router(userRouter, prefix="/api/v1", tags=["User"])

