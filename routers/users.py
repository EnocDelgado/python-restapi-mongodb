from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",tags=["users"], responses={404: {"message": "Not Found"}})

# User entry
class User(BaseModel):
    id: int 
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name='Eld', surname='Kolm', url='http://eld.org', age=20),
              User(id=2, name='Elf', surname='Halm', url='http://elf.com', age=30),
              User(id=3, name='Elv', surname='Fulm', url='http://elv.io', age=35),
]

@router.get("/")
async def users():
    return users_list

# Path
@router.get("/{id}")
async def user(id: int):
    return search_user(id)

# Query
# localhost:port/userquery/?id=1
@router.get("/")
async def user(id: int):
    return search_user(id)


# Create a new user
@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="User already exists")
    
    users_list.append(user)
    return user


# Update an user
@router.put("/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "User not updated"}
    
    return user


# Delete an user
@router.delete("/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "User not deleted"}
    
    
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}