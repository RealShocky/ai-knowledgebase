import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Box,
  Rating,
  TextField,
  Button,
  Chip,
  Divider,
  IconButton,
} from '@mui/material';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import axios from 'axios';

interface Article {
  id: number;
  title: string;
  content: string;
  category: string;
  tags: string[];
}

interface ArticleViewerProps {
  article: Article;
  onClose?: () => void;
}

export const ArticleViewer: React.FC<ArticleViewerProps> = ({
  article,
  onClose,
}) => {
  const [rating, setRating] = useState<number | null>(null);
  const [feedback, setFeedback] = useState('');
  const [helpful, setHelpful] = useState<boolean | null>(null);

  const handleSubmitFeedback = async () => {
    try {
      await axios.post(`/api/articles/${article.id}/feedback`, {
        rating,
        comment: feedback,
        helpful,
      });
      // Show success message or reset form
      setRating(null);
      setFeedback('');
      setHelpful(null);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  return (
    <Paper sx={{ p: 3, maxWidth: 800, margin: '0 auto' }}>
      <Typography variant="h4" gutterBottom>
        {article.title}
      </Typography>

      <Box sx={{ mb: 2 }}>
        <Chip label={article.category} sx={{ mr: 1 }} />
        {article.tags.map((tag) => (
          <Chip key={tag} label={tag} variant="outlined" sx={{ mr: 1 }} />
        ))}
      </Box>

      <Box sx={{ mb: 4 }}>
        <ReactMarkdown
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || '');
              return !inline && match ? (
                <SyntaxHighlighter
                  style={materialDark}
                  language={match[1]}
                  PreTag="div"
                  {...props}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
          }}
        >
          {article.content}
        </ReactMarkdown>
      </Box>

      <Divider sx={{ my: 3 }} />

      <Typography variant="h6" gutterBottom>
        Was this article helpful?
      </Typography>

      <Box sx={{ mb: 2 }}>
        <IconButton
          color={helpful === true ? 'primary' : 'default'}
          onClick={() => setHelpful(true)}
        >
          <ThumbUpIcon />
        </IconButton>
        <IconButton
          color={helpful === false ? 'primary' : 'default'}
          onClick={() => setHelpful(false)}
        >
          <ThumbDownIcon />
        </IconButton>
      </Box>

      <Box sx={{ mb: 2 }}>
        <Typography component="legend">Rate this article</Typography>
        <Rating
          value={rating}
          onChange={(event, newValue) => {
            setRating(newValue);
          }}
        />
      </Box>

      <TextField
        fullWidth
        multiline
        rows={4}
        variant="outlined"
        placeholder="Share your feedback (optional)"
        value={feedback}
        onChange={(e) => setFeedback(e.target.value)}
        sx={{ mb: 2 }}
      />

      <Button
        variant="contained"
        color="primary"
        onClick={handleSubmitFeedback}
        disabled={!helpful && !rating && !feedback}
      >
        Submit Feedback
      </Button>
    </Paper>
  );
};

export default ArticleViewer;
