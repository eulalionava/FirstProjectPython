from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime,timedelta

from jose import jwt,JWTError

ALGORITMO = "HS256"
ACCESS_TOKEN_DURATION = 2
SECRET = "7575ufodsfochsdofud09"


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username:str
    full_name:str
    email:str
    disable:bool

class UserDB(User):
    password:str


users_db = {
    "eulalio":{
        "username":"eulalio",
        "full_name":"eulalio nava",
        "email":"eulalio@gmail.com",
        "disable":False,
        "password":"$2a$12$AZKfydK0ro/cloHJtZPbru3MGWlssyWapKwv8brbBr2H2xFgdysUS"
    },
    "eulalio2":{
        "username":"eulalio2",
        "full_name":"eulalio nava2",
        "email":"eulalio2@gmail.com",
        "disable":True,
        "password":"$2a$12$AZKfydK0ro/cloHJtZPbru3MGWlssyWapKwv8brbBr2H2xFgdysUS"
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])
    

async def auth_user(token:str = Depends(oauth2)):
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de authenticación invalidas",
            headers={"www-authenticate":"Bearer"})
    try:
        username = jwt.decode(token,SECRET,algorithms=[ALGORITMO]).get("sub")
        print(username)
        if username is None:
            return exception
        
    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user:User = Depends(auth_user)):
    if user.disable:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario inactivo")

    return user


@router.post("/login")
async def login(form:OAuth2PasswordRequestForm=Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    crypt.verify(form.password,user.password)

    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña no es correcta")
    

    access_token = {"sub":user.username,
                    "exp":datetime.now() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    
    return {"access_token":jwt.encode(access_token,SECRET,algorithm=ALGORITMO),"token_type":"bearer"}

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user