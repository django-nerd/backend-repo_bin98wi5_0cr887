import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Book

app = FastAPI(title="Books & Audio Summaries API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Books & Audio Summaries Backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Models for requests
class BookCreate(Book):
    pass

class BookFilter(BaseModel):
    category: Optional[str] = None
    q: Optional[str] = None  # search in title/author/description
    limit: Optional[int] = 50

@app.post("/api/books")
def create_book(book: BookCreate):
    try:
        inserted_id = create_document("book", book)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/books/search")
def search_books(filter: BookFilter):
    try:
        query = {}
        if filter.category:
            query["category"] = filter.category
        if filter.q:
            query["$or"] = [
                {"title": {"$regex": filter.q, "$options": "i"}},
                {"author": {"$regex": filter.q, "$options": "i"}},
                {"description": {"$regex": filter.q, "$options": "i"}},
                {"tags": {"$elemMatch": {"$regex": filter.q, "$options": "i"}}}
            ]
        books = get_documents("book", query, limit=filter.limit or 50)
        # Convert ObjectId to str for JSON
        for b in books:
            if isinstance(b.get("_id"), ObjectId):
                b["id"] = str(b.pop("_id"))
        return {"items": books}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/books")
def list_books(category: Optional[str] = None, q: Optional[str] = None, limit: int = 50):
    try:
        query = {}
        if category:
            query["category"] = category
        if q:
            query["$or"] = [
                {"title": {"$regex": q, "$options": "i"}},
                {"author": {"$regex": q, "$options": "i"}},
                {"description": {"$regex": q, "$options": "i"}},
                {"tags": {"$elemMatch": {"$regex": q, "$options": "i"}}}
            ]
        books = get_documents("book", query, limit=limit)
        for b in books:
            if isinstance(b.get("_id"), ObjectId):
                b["id"] = str(b.pop("_id"))
        return {"items": books}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
