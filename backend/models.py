from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Product(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
    category_id: Optional[str] = None # Changed from 'category' to 'category_id'
    restaurant_slug: str # Added for multi-tenancy

    class Config:
        populate_by_name = True # Renamed from allow_population_by_field_name in Pydantic V2
        json_schema_extra = {
            "example": {
                "name": "Pizza Margherita",
                "description": "Classic pizza with tomato and mozzarella.",
                "price": 12.50,
                "image": "https://example.com/pizza.jpg",
                "category_id": "60d5ec49f8c7b7e8a0b8c7b7",
                "restaurant_slug": "myrestaurant"
            }
        }