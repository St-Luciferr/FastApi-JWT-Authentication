from fastapi import HTTPException, Depends, APIRouter, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.security import OAuth2PasswordBearer,  HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from starlette import status
from sqlalchemy.orm import Session

from models.schemas import RefereshToken, User, LoginData
from models.database import get_db, engine
from models.models import Base
from models.models import UserDB as UserInDB
from .utils import hash_password, verify_password
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

userRouter = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
api_key_header = APIKeyHeader(name="Authorization")

Base.metadata.create_all(bind=engine)


@userRouter.post("/register-user")
def register_user(user: User, db: Session = Depends(get_db)):
    try:
        db_user = db.query(UserInDB).filter(UserInDB.email == user.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        new_user = user.dict()
        new_user["password"] = hash_password(new_user["password"])

        db_user = UserInDB(**new_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse(content={"message": "User registered successfully"}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error registering user: {e}")


@userRouter.post("/auth/login")
async def login_user(form_data: LoginData, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    try:
        user = db.query(UserInDB).filter(
            UserInDB.email == form_data.email).first()
        if not user:
            raise HTTPException(status_code=400, detail="User does not exist")

        if not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid password")

        access_token = Authorize.create_access_token(subject=user.email)
        refresh_token = Authorize.create_refresh_token(subject=user.email)

        return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token}, status_code=status.HTTP_200_OK)
    except AuthJWTException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error logging in")


@userRouter.post("/auth/refresh-token")
def refresh_token(
    form_data: RefereshToken,
    Authorize: AuthJWT = Depends()
):
    try:
        Authorize._token = form_data.refresh_token
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        acccess_token = Authorize.create_access_token(subject=current_user)
        return JSONResponse(content={"access_token": acccess_token}, status_code=status.HTTP_200_OK)
    except AuthJWTException as e:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Authentication error :{e}")


security = HTTPBearer()
def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    Authorize = AuthJWT()
    Authorize._token = credentials.credentials
    Authorize.jwt_required()
    return Authorize.get_jwt_subject()


@userRouter.get("/me")
def read_user_me(
        token: str = Depends(verify_token),
        db: Session = Depends(get_db),
        Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required(token=token)
        current_user = Authorize.get_jwt_subject()
        user = db.query(UserInDB).filter(
            UserInDB.email == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        result = user.__dict__.copy()
        result.pop("_sa_instance_state")
        result.pop("password")
        result.pop("id")
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except AuthJWTException as e:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Authentication error :{e}")
