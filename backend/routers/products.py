from fastapi import APIRouter, HTTPException, Depends
from typing import List
from models import Product
from services.products import ProductService
from db.mongo import database

router = APIRouter()

# Dependency to get ProductService
async def get_product_service():
    return ProductService(database)

@router.get("/products", response_model=List[Product])
async def get_products(product_service: ProductService = Depends(get_product_service)):
    # For now, we'll use a placeholder slug. In a multi-tenant app, this would come from auth.
    products = await product_service.get_products_by_restaurant(slug="default_restaurant_slug")
    return products

@router.post("/products", response_model=Product)
async def create_product(product: Product, product_service: ProductService = Depends(get_product_service)):
    # For now, we'll use a placeholder slug.
    created_product = await product_service.create_product(slug="default_restaurant_slug", product_data=product)
    return created_product
