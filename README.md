# FAQRep - AI-Powered VPN Support Knowledge Base

An intelligent support knowledge base that uses AI to help users find answers to their VPN-related questions quickly and accurately.

## Features

- **AI-Powered Search**: Utilizes Claude API for semantic search and intelligent query understanding
- **Keyword Fallback**: Maintains functionality even when AI services are unavailable
- **Markdown Support**: Content stored in easy-to-maintain markdown format
- **Modern UI**: Clean, responsive interface built with React
- **Fast Backend**: High-performance FastAPI backend with SQLite database
- **Real-time Updates**: Hot-reloading for both frontend and backend during development

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Claude API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/faqrep.git
cd faqrep
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the backend directory with:
```
CLAUDE_API_KEY=your_api_key_here
```

4. Initialize the database:
```bash
python init_db.py
```

5. Set up the frontend:
```bash
cd ../frontend
npm install
```

### Running the Application

1. Start the backend server:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
faqrep/
├── backend/
│   ├── articles/       # Markdown content
│   ├── ai_engine.py    # Claude API integration
│   ├── main.py         # FastAPI application
│   ├── models.py       # Database models
│   ├── search.py       # Search functionality
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── App.js
    │   └── index.js
    └── package.json
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
