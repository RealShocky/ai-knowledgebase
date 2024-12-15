from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from dotenv import load_dotenv
import os
from database import get_db, init_db
from search import SearchEngine
from ai_engine import AIEngine
from models import Article
import markdown2
from sqlalchemy.orm import Session

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="FAQRep API", description="AI-Powered VPN Support Platform API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI engine
ai_engine = AIEngine()

class SearchQuery(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None

@app.get("/")
async def root():
    return {"message": "Welcome to FAQRep API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/search")
async def search_knowledge_base(query: SearchQuery, db: Session = Depends(get_db)):
    try:
        search_engine = SearchEngine(db, ai_engine)
        results = await search_engine.search(query.query, query.filters)
        return {"results": results}
    except Exception as e:
        print(f"Search error: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/articles/{article_id}")
async def get_article(article_id: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "category": article.category,
        "tags": [tag.name for tag in article.tags]
    }

if __name__ == "__main__":
    # Initialize the database
    init_db()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
