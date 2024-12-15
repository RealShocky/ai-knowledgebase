from database import init_db, get_db_session
from models import Article, Tag, Base
from sqlalchemy import create_engine
import re
import os
import markdown2
from ai_engine import AIEngine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug: Print API key (first few characters)
api_key = os.getenv("CLAUDE_API_KEY")
if api_key:
    print(f"API Key found: {api_key[:10]}...")
else:
    print("No API key found!")

def slugify(title):
    # Convert to lowercase and replace spaces with hyphens
    slug = title.lower()
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

def parse_markdown_file(file_path):
    """Parse a markdown file and extract metadata and content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into lines
    lines = content.split('\n')
    
    # Extract title (first h1)
    title = None
    for line in lines:
        if line.startswith('# '):
            title = line.lstrip('# ').strip()
            break
    
    if not title:
        # Use filename as title if no h1 found
        title = os.path.splitext(os.path.basename(file_path))[0].replace('-', ' ').title()
    
    # Extract category and tags
    category = None
    tags = []
    content_lines = []
    
    in_metadata = False
    for line in lines:
        if line.startswith('## Category:'):
            category = line.replace('## Category:', '').strip()
        elif line.startswith('## Tags:'):
            tags = [tag.strip() for tag in line.replace('## Tags:', '').split(',')]
        else:
            content_lines.append(line)
    
    # Convert markdown to HTML
    html_content = markdown2.markdown('\n'.join(content_lines))
    
    return {
        'title': title,
        'category': category or 'Uncategorized',
        'tags': tags,
        'content': html_content,
        'raw_content': '\n'.join(content_lines)  # Store raw markdown for embedding
    }

def create_initial_data():
    """Create initial articles from markdown files"""
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')
    
    if not os.path.exists(docs_dir):
        print(f"Docs directory not found at {docs_dir}")
        return
    
    with get_db_session() as db:
        # Create tables
        Base.metadata.create_all(db.get_bind())
        
        # Clear existing data
        db.query(Article).delete()
        db.query(Tag).delete()
        db.commit()
        
        ai_engine = AIEngine()
        
        # Process each markdown file
        for filename in os.listdir(docs_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(docs_dir, filename)
                print(f"Processing {filename}...")
                
                try:
                    data = parse_markdown_file(file_path)
                    
                    # Create article
                    article = Article(
                        title=data['title'],
                        slug=slugify(data['title']),
                        category=data['category'],
                        content=data['content']
                    )
                    
                    # Create tags
                    for tag_name in data['tags']:
                        tag = db.query(Tag).filter_by(name=tag_name).first()
                        if not tag:
                            tag = Tag(name=tag_name)
                            db.add(tag)
                        article.tags.append(tag)
                    
                    db.add(article)
                    db.commit()
                    
                    # Generate and store embedding
                    embedding = ai_engine.get_embedding(data['raw_content'])
                    article.embedding = embedding.tobytes()
                    db.commit()
                    
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
                    db.rollback()

if __name__ == "__main__":
    print("Initializing database...")
    # Remove existing database if it exists
    if os.path.exists("faqrep.db"):
        os.remove("faqrep.db")
    
    # Initialize database
    create_initial_data()
    print("Database initialization complete!")
