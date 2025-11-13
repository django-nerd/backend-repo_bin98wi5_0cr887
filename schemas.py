"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Book(BaseModel):
    """
    Books collection schema
    Collection name: "book"
    """
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Author name")
    category: str = Field(..., description="Category/genre (e.g., Fiction, History)")
    description: Optional[str] = Field(None, description="Short description or summary")
    cover_image_url: Optional[HttpUrl] = Field(None, description="Cover image URL")
    content: Optional[str] = Field(None, description="Readable text content or long summary")
    audio_summary_url: Optional[HttpUrl] = Field(None, description="URL to an audio summary file (MP3, etc.)")
    tags: Optional[List[str]] = Field(default=None, description="Keywords or tags")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
