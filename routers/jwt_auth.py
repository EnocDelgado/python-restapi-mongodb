from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "Q3ZW4XE5CR6V7TB879N809OKPS34D5g687h89pjon"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "thebiger": {
        "username": "thebiger",
        "fullname": "Maco McGregor",
        "email": "macomacgregor@mail.com",
        "disabled": False,
        "password": "$2a$12$aLge9dSsqWJW5XfjeVY75u5CQvTGwB6S2MEzs/m9rDG5b4q3g5Om2"
    },
    "carlos": {
        "username": "carlos",
        "fullname": "Carlos Chile",
        "email": "carloschile@mail.com",
        "disabled": True,
        "password": "$2a$12$zp7LkQMuoRc8jSOH2oCtIeziUYhvXrg5PW72fFxKvlQPbexzgUpzy"
    }
}

# Verify if exist an user in our database
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Wrong authentication credentials", 
            headers={"WWW-Authenticate": "Bearer"})
        
    try:
        username  = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")

        if  username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)

# Dependency criteria
async def current_user(user: User = Depends(auth_user)):  
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user is disabled")

    return user

# Authenticate an user
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect username")

    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect password")

    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


# Tell the user wich is its user
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user