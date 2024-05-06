
# ChatBot Application with FastAPI and OpenAI

## Overview
This application uses FastAPI to create a web-based chat interface that interacts with OpenAI's GPT models. It includes real-time chatting capabilities with AI-generated responses that ensure relevance and accuracy through predefined responses validation.

## Features
- Web-based chat interface
- Interaction with OpenAI's GPT models
- Response validation using a predefined set of responses
- Response confidence calculation
- Response time tracking

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/louisdesc/ChatGPT-FastAPI-Interface
   ```
   
2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn jinja2 openai
   ```

3. **Run the application:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   Navigate to `http://127.0.0.1:8000/chat` to access the chat interface.

## Files Description
- `main.py`: Contains FastAPI app setup, routes, and chat logic.
- `chat_logic.py`: Includes helper functions for importing data, formatting conversations, calculating confidence, and verifying responses.

## Contributions
Contributions are welcome. Please create a pull request or raise an issue for bugs and feature requests.

