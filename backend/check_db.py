from database import get_db_session
from models import Article, Tag

def check_database():
    with get_db_session() as db:
        articles = db.query(Article).all()
        print(f"\nFound {len(articles)} articles:")
        for article in articles:
            print(f"\nTitle: {article.title}")
            print(f"Category: {article.category}")
            print(f"Tags: {[tag.name for tag in article.tags]}")
            print(f"Content length: {len(article.content)} chars")
            print("-" * 50)

if __name__ == "__main__":
    check_database()
