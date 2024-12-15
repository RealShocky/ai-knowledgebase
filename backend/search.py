from models import Article, SearchLog
from database import get_db_session
import numpy as np
from ai_engine import AIEngine
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import re

class SearchEngine:
    def __init__(self, db: Session, ai_engine: AIEngine):
        self.db = db
        self.ai_engine = ai_engine

    async def search(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Perform a search using keyword-based search
        """
        try:
            # Log the search query
            search_log = SearchLog(query=query)
            self.db.add(search_log)
            self.db.commit()
            
            # Get search results
            results = self.search_articles(query, limit=page_size)
            
            return results
            
        except Exception as e:
            print(f"Search error: {str(e)}")
            self.db.rollback()
            raise

    def search_articles(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for articles using keyword matching
        """
        try:
            # Fallback to keyword search
            query_terms = query.lower().split()
            results = []
            articles = self.db.query(Article).all()
            
            for article in articles:
                # Calculate simple relevance score based on term frequency
                content = article.content.lower()
                title = article.title.lower()
                
                score = 0
                for term in query_terms:
                    # Title matches are weighted more heavily
                    title_matches = title.count(term) * 3
                    content_matches = content.count(term)
                    score += title_matches + content_matches
                
                if score > 0:
                    results.append((article, score))
            
            # Sort by score
            results.sort(key=lambda x: x[1], reverse=True)
            
            # Log the search
            search_log = SearchLog(
                query=query,
                results_count=len(results[:limit])
            )
            self.db.add(search_log)
            self.db.commit()
            
            # Return top results
            return [
                {
                    "id": article.id,
                    "title": article.title,
                    "content": article.content,
                    "category": article.category,
                    "tags": [tag.name for tag in article.tags],
                    "relevance": float(score)
                }
                for article, score in results[:limit]
            ]
            
        except Exception as e:
            self.db.rollback()
            print(f"Search error: {str(e)}")
            return []

    async def get_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions based on partial query
        """
        try:
            # Get all articles
            articles = self.db.query(Article).all()
            
            # Extract words from titles and content
            words = set()
            for article in articles:
                title_words = article.title.lower().split()
                words.update(word for word in title_words if word.startswith(query.lower()))
            
            return sorted(list(words))[:5]  # Return top 5 suggestions
            
        except Exception as e:
            print(f"Error getting suggestions: {str(e)}")
            return []
