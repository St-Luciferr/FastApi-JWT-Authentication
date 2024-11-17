from datetime import  timedelta
import bcrypt
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import os
import dotenv
from config import BASE_PATH
dotenv.load_dotenv()

RSA_PRIVATE_KEY_PATH = os.getenv("RSA_PRIVATE_KEY_PATH")
RSA_PUBLIC_KEY_PATH = os.getenv("RSA_PUBLIC_KEY_PATH")

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

PRIVATE_KEY_PATH = os.path.join(BASE_PATH, RSA_PRIVATE_KEY_PATH)
PUBLIC_KEY_PATH = os.path.join(BASE_PATH, RSA_PUBLIC_KEY_PATH)
with open(PRIVATE_KEY_PATH, "r") as private_key_file:
    private_key = private_key_file.read()

with open(PUBLIC_KEY_PATH, "r") as public_key_file:
    public_key = public_key_file.read()


class Settings(BaseModel):
    authjwt_private_key: str = private_key  # Path to private key for signing
    authjwt_public_key: str = public_key  # Path to public key for verification
    authjwt_algorithm: str = "RS256"       # RSA signing algorithm
    authjwt_access_token_expires: int = 3600  #


# Initialize AuthJWT with configuration
@AuthJWT.load_config
def get_config():
    return Settings()


def hash_password(password: str):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(subject, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    access_token = AuthJWT.create_access_token(
        subject=subject, expires_time=expires_delta)
    return access_token


# Utility function to create refresh tokens
def create_refresh_token(subject, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)):
    refresh_token = AuthJWT.create_refresh_token(
        subject=subject, expires_time=expires_delta)
    return refresh_token
