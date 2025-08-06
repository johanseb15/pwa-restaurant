from typing import List, Optional
from bson import ObjectId
from db.mongo import database # Keep this import for type hinting, but don't use directly in __init__
from models import Product

class ProductService:
    def __init__(self, db_client):
        self.collection = db_client["products"]

    async def get_products_by_restaurant(self, slug: str, category_id: Optional[str] = None, search: Optional[str] = None, popular_only: bool = False) -> List[Product]:
        query = {"restaurant_slug": slug}
        if category_id:
            query["category_id"] = category_id
        if search:
            query["name"] = {"$regex": search, "$options": "i"}
        if popular_only:
            pass
        
        products = []
        async for product_data in self.collection.find(query):
            # Ensure _id is converted to string for Pydantic model
            product_data["id"] = str(product_data["_id"])
            products.append(Product(**product_data))
        return products

    async def get_product_by_id(self, product_id: str, slug: str) -> Optional[Product]:
        product_data = await self.collection.find_one({"_id": ObjectId(product_id), "restaurant_slug": slug})
        if product_data:
            product_data["id"] = str(product_data["_id"])
            return Product(**product_data)
        return None

    async def create_product(self, slug: str, product_data: Product) -> Product:
        product_data_dict = product_data.model_dump(by_alias=True, exclude_none=True)
        product_data_dict["restaurant_slug"] = slug
        result = await self.collection.insert_one(product_data_dict)
        product_data.id = str(result.inserted_id)
        return product_data

    async def update_product(self, product_id: str, product_data: Product) -> bool:
        update_data = product_data.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0

    async def delete_product(self, product_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0