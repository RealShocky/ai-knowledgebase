from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean, LargeBinary
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Association table for article tags
article_tags = Table(
    'article_tags',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(LargeBinary)  # Store embeddings as binary data
    slug = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    category = Column(String(100))
    is_published = Column(Boolean, default=True)
    
    tags = relationship('Tag', secondary=article_tags, back_populates='articles')
    feedback = relationship('Feedback', back_populates='article')

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    articles = relationship('Article', secondary=article_tags, back_populates='tags')

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    rating = Column(Integer)  # 1-5 rating
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    article = relationship('Article', back_populates='feedback')

class SearchLog(Base):
    __tablename__ = 'search_logs'
    
    id = Column(Integer, primary_key=True)
    query = Column(String(255))
    results_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
