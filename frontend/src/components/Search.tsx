import React, { useState, useEffect } from 'react';
import {
  TextField,
  Paper,
  List,
  ListItem,
  ListItemText,
  Typography,
  Chip,
  Box,
  CircularProgress,
  Autocomplete,
} from '@mui/material';
import { debounce } from 'lodash';
import axios from 'axios';

interface SearchResult {
  id: number;
  title: string;
  content: string;
  category: string;
  tags: string[];
  relevance_score: number;
}

interface SearchProps {
  onResultSelect?: (result: SearchResult) => void;
}

export const Search: React.FC<SearchProps> = ({ onResultSelect }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [availableTags, setAvailableTags] = useState<string[]>([]);

  const performSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('/api/search', {
        query: searchQuery,
        filters: {
          tags: selectedTags,
        },
      });
      setResults(response.data.results);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const debouncedSearch = debounce(performSearch, 300);

  const fetchSuggestions = async (input: string) => {
    try {
      const response = await axios.get(`/api/suggestions?query=${input}`);
      setSuggestions(response.data);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
    }
  };

  const debouncedFetchSuggestions = debounce(fetchSuggestions, 200);

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await axios.get('/api/tags');
        setAvailableTags(response.data);
      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    };
    fetchTags();
  }, []);

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newQuery = event.target.value;
    setQuery(newQuery);
    debouncedSearch(newQuery);
    debouncedFetchSuggestions(newQuery);
  };

  const handleTagChange = (event: React.ChangeEvent<{}>, newTags: string[]) => {
    setSelectedTags(newTags);
    if (query) {
      debouncedSearch(query);
    }
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 800, margin: '0 auto' }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search knowledge base..."
        value={query}
        onChange={handleQueryChange}
        sx={{ mb: 2 }}
      />

      <Autocomplete
        multiple
        options={availableTags}
        value={selectedTags}
        onChange={handleTagChange}
        renderInput={(params) => (
          <TextField
            {...params}
            variant="outlined"
            placeholder="Filter by tags..."
          />
        )}
        sx={{ mb: 2 }}
      />

      {loading && (
        <Box display="flex" justifyContent="center" my={2}>
          <CircularProgress />
        </Box>
      )}

      {suggestions.length > 0 && query && (
        <Paper sx={{ mb: 2 }}>
          <List>
            {suggestions.map((suggestion, index) => (
              <ListItem
                button
                key={index}
                onClick={() => {
                  setQuery(suggestion);
                  performSearch(suggestion);
                }}
              >
                <ListItemText primary={suggestion} />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {results.length > 0 && (
        <Paper>
          <List>
            {results.map((result) => (
              <ListItem
                key={result.id}
                button
                onClick={() => onResultSelect?.(result)}
                sx={{ flexDirection: 'column', alignItems: 'flex-start' }}
              >
                <Typography variant="h6">{result.title}</Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                  }}
                >
                  {result.content}
                </Typography>
                <Box sx={{ mt: 1 }}>
                  {result.tags.map((tag) => (
                    <Chip
                      key={tag}
                      label={tag}
                      size="small"
                      sx={{ mr: 0.5 }}
                    />
                  ))}
                </Box>
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
};

export default Search;
