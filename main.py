from fastapi import FastAPI
from routers import products, users, jwt_auth, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# start server: uvicorn main:app --reload

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth.router)
app.include_router(users_db.router)


# display resources statics 
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI"}

