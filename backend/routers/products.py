from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from models import Product, ProductCreate, ProductResponse
from services.products import ProductService
from db.mongo import database
from dependencies import get_current_admin_user # Import get_current_admin_user from dependencies

router = APIRouter()

# Dependency to get ProductService
async def get_product_service():
    return ProductService(database)

@router.get("/products", response_model=List[ProductResponse])
async def get_products(product_service: ProductService = Depends(get_product_service), current_user: dict = Depends(get_current_admin_user)):
    products = await product_service.get_products_by_restaurant(slug=current_user["restaurant_slug"])
    return products

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, product_service: ProductService = Depends(get_product_service), current_user: dict = Depends(get_current_admin_user)):
    created_product = await product_service.create_product(slug=current_user["restaurant_slug"], product_data=product)
    return created_product
