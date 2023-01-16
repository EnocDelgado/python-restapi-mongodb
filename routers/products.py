from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["poducts"], responses={404: {"message": "Not Found"}})

product_lists = ["Product 1", "Product 2", "Product 3", "Product 4", "Product 5"]

@router.get("/")
async def products():
    return product_lists


#
@router.get("/{id}")
async def product(id: int):
    return product_lists[id]