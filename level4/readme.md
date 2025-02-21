# Movie Character Chatbot 🎬🤖

A scalable backend chatbot that lets users interact with movie characters using RAG, PostgreSQL, ChromaDB, and Gemini AI.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)](https://fastapi.tiangolo.com)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [File Structure](#file-structure)
- [API Documentation](#api-documentation)
- [Redis Setup](#redis-setup)
- [ChromaDB Setup](#chromadb-setup)
- [Load Testing with Locust](#load-testing-with-locust)
- [License](#license)

## Features

- Character-specific responses using Gemini AI
- Hybrid search (Vector + Keyword)
- Rate limiting (5 requests/sec)
- Redis caching
- Async database operations
- Load test ready

## Prerequisites

- Python 3.9+
- PostgreSQL 14+
- Redis 7+
- Google Gemini API Key

## Installation

```bash
# Clone repository
git clone https://github.com/yourusername/movie-character-bot.git
cd movie-character-bot

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt


Configuration
Create .env file:
```

## Configuration

Create .env file:

# PostgreSQL

        DB_NAME=moviebot
        DB_USER=postgres
        DB_PASSWORD=your@password
        DB_HOST=localhost
        DB_PORT=5432

# Redis

        REDIS_URL=redis://localhost:6379

# Gemini

        GEMINI_API_KEY=your_api_key_here

## Running the Project

# Start Redis (new terminal)

        redis-server

# Start FastAPI server

        uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# In another terminal - Run Locust load test

        locust -f locustfile.py

## File Structure

        moviebot/
        ├── app.py                 # Main FastAPI application
        ├── config.py              # Environment configuration
        ├── database.py            # PostgreSQL database setup
        ├── chroma_setup.py        # ChromaDB vector store setup
        ├── gemini_utils.py        # Gemini AI integration
        ├── cache.py               # Redis caching layer
        ├── rate_limit.py          # Rate limiting configuration
        ├── locustfile.py          # Load testing scenarios
        ├── requirements.txt       # Dependency list
        └── .env                   # Environment variables

### API Documentation

#### POST /chat

        Chat with a movie character

#### Request:

        {
        "character": "Tony Stark",
        "user_message": "How to build an arc reactor?"
        }

#### Response:

        {
        "response": "First, you need a palladium core... but maybe start with something simpler. Try a miniaturized toroidal field generator."
                }

### Redis Setup

#### Linux (Ubuntu)

        sudo apt install redis-server
        sudo systemctl start redis

#### Windows (WSL)

        wsl --install
        sudo apt update && sudo apt install redis-server
        sudo service redis-server start

#### Verify

        redis-cli ping  # Should return "PONG"
        ChromaDB Setup

#### Create vector store

        python chroma_setup.py

#### Expected output

        Loaded 20000 dialogues
        Created collection 'dialogues' with 384-dim embeddings

### Load Testing with Locust

#### Install Locust

        pip install locust

#### Run headless test (1000 users, 100 spawn rate)

        locust -f locustfile.py --headless -u 1000 -r 100 --host http://localhost:8000

#### Web UI mode (http://localhost:8089)

        locust -f locustfile.py

### License

        MIT License - See LICENSE for details
