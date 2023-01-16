from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "maryallstar": {
        "username": "maryallstar",
        "fullname": "Mary McGregor",
        "email": "marymacgregor@mail.com",
        "disabled": False,
        "password": "12345"
    },
    "thebiger": {
        "username": "thebiger",
        "fullname": "Maco McGregor",
        "email": "macomacgregor@mail.com",
        "disabled": False,
        "password": "12345"
    },
    "carlos": {
        "username": "carlos",
        "fullname": "Carlos Chile",
        "email": "carloschile@mail.com",
        "disabled": False,
        "password": "54321"
    }
}


# Verify if exist an user in our database
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


# Dependency criteria
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Wrong authentication credentials", 
            headers={"WWW-Authenticate": "Bearer"})
    
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
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect password")

    return {"access_token": user.username, "token_type": "bearer"}


# Tell the user wich is its user
@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user