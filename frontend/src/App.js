import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          filters: {}
        }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error('Error:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>VPN Support Knowledge Base</h1>
      </header>
      <main className="App-main">
        <div className="search-container">
          <form onSubmit={handleSearch}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search FAQs..."
              className="search-input"
            />
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? 'Searching...' : 'Search'}
            </button>
          </form>
        </div>
        
        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}
        
        {loading && <div className="loading">Searching...</div>}
        
        {results && results.length === 0 && !loading && (
          <div className="no-results">
            No results found for your query.
          </div>
        )}
        
        {results && results.length > 0 && (
          <div className="results-container">
            {results.map((result, index) => (
              <div key={index} className="result-card">
                <h2>{result.title}</h2>
                <p className="metadata">
                  Category: {result.category} | Tags: {result.tags ? result.tags.join(', ') : 'None'}
                </p>
                <div className="content" dangerouslySetInnerHTML={{ __html: result.content }} />
                <div className="relevance">Relevance Score: {Math.round(result.relevance * 100)}%</div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
