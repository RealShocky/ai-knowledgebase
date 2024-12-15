from langchain_community.vectorstores import FAISS
from langchain.text_splitter import MarkdownTextSplitter
from langchain.memory import ConversationBufferMemory
import os
from typing import List, Dict, Any
import json
from anthropic import Anthropic
import numpy as np

class AIEngine:
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY environment variable not set")
        self.anthropic = Anthropic(api_key=self.api_key)
        self.embedding_model = "claude-2"
        self.embedding_dimension = 1536  # Claude's embedding dimension
        self.text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vector_store = None

    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a text using Claude API"""
        try:
            # Normalize text
            text = text.replace("\n", " ").strip()
            
            # Get embedding from Claude
            response = self.anthropic.messages.create(
                model=self.embedding_model,
                max_tokens=1000,
                system="Generate a vector embedding for the following text. Return only the embedding as a list of 1536 numbers.",
                messages=[{"role": "user", "content": text}]
            )
            
            # Parse response and convert to numpy array
            embedding = json.loads(response.content[0].text)
            return np.array(embedding, dtype=np.float32)
            
        except Exception as e:
            print(f"Error getting embedding: {str(e)}")
            # Return zero vector as fallback
            return np.zeros(self.embedding_dimension, dtype=np.float32)

    def answer_question(self, question: str, context: str) -> str:
        """Generate an answer to a question given some context"""
        try:
            response = self.anthropic.messages.create(
                model=self.embedding_model,
                max_tokens=1000,
                system="You are a helpful assistant answering questions about VPN services. Use the provided context to answer questions accurately and concisely.",
                messages=[
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            return "I apologize, but I encountered an error while trying to generate an answer. Please try again."

    def initialize_vector_store(self, documents: List[Dict[str, str]]):
        """Initialize FAISS vector store with documents"""
        texts = []
        metadatas = []
        
        for doc in documents:
            chunks = self.text_splitter.split_text(doc["content"])
            texts.extend(chunks)
            metadatas.extend([{"title": doc["title"], "id": doc["id"]} for _ in chunks])
        
        if texts:
            # Use Claude to get embeddings for each text chunk
            embeddings = []
            for text in texts:
                embedding = self.get_embedding(text)
                embeddings.append(embedding)
            
            # Create FAISS index with the embeddings
            self.vector_store = FAISS.from_embeddings(
                text_embeddings=list(zip(texts, embeddings)),
                embedding=None,
                metadatas=metadatas
            )

    def search(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        if not self.vector_store:
            return []
        
        # Get query embedding using Claude
        query_embedding = self.get_embedding(query)
        
        # Perform similarity search
        docs_with_scores = self.vector_store.similarity_search_with_score_by_vector(query_embedding, k=5)
        
        # Process results
        results = []
        for doc, score in docs_with_scores:
            # Get AI-enhanced answer for this document
            context = doc.page_content
            answer = self.answer_question(query, context)
            
            result = {
                "content": answer,
                "title": doc.metadata.get("title", ""),
                "id": doc.metadata.get("id", ""),
                "score": float(score)
            }
            results.append(result)
        
        return results
