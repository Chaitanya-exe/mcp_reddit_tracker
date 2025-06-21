# Reddit Trend Tracker (MCP)

## Overview

Reddit Trend Tracker is an AI-powered tool built using the Model Context Protocol (MCP) architecture that allows users to analyze and gain insights from Reddit content. The application fetches posts from specified subreddits and uses an LLM (Large Language Model) to analyze trends, answer questions, and provide insights about the content.

The project follows a client-server architecture with:

- **MCP Server**: Handles Reddit API interactions and exposes tools for fetching posts
- **MCP Client**: Manages user interactions, LLM integration, and tool execution

## Features

- Fetch top posts from any subreddit through Reddit's OAuth API
- Query the data with natural language questions
- Get AI-powered analysis of subreddit trends and content
- Interactive command-line interface for easy use

## Architecture

The application uses the Model Context Protocol (MCP) which enables structured communication between the client and server components:

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │  MCP    │             │  API    │             │
│  LLM Client ├─────────┤  MCP Server ├─────────┤  Reddit API │
│             │         │             │         │             │
└─────────────┘         └─────────────┘         └─────────────┘
```

### Components

1. **MCP Server**
   - Implements Reddit API authentication and post fetching
   - Exposes tools through MCP protocol
   - Handles data formatting and server operations

2. **MCP Client**
   - Manages user interaction through CLI
   - Integrates with Ollama for LLM capabilities
   - Handles tool calling and result processing

## Prerequisites

- Python 3.9+ (3.13 recommended)
- Reddit API credentials
- Ollama installed (for local LLM support)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd trend_tracker_mcp
```

### 2. Set up environment variables

Create a `.env` file in the project root with your Reddit API credentials:

```env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USERNAME=your_reddit_username
PASSWORD=your_reddit_password
```

### 3. Install dependencies for server

```bash
cd mcp_server
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Install dependencies for client

```bash
cd ../mcp_client
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Running the application

Start the client application (the server will be started automatically):

```bash
cd mcp_client
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

### 2. Asking questions

Once the application is running, you can ask questions about specific subreddits:

```
Ask about some content on a specific subreddit: What are the top trends in r/Python right now?
```

The application will:
1. Process your query using LLM
2. Identify the need to fetch data from the specified subreddit
3. Call the appropriate MCP tool
4. Fetch the content from Reddit
5. Send the content back to the LLM for analysis
6. Present the final response

## Example Queries

- "What are people discussing in r/MachineLearning this week?"
- "Summarize the top 5 posts from r/AskScience"
- "Are there any recurring themes in r/ProgrammerHumor?"
- "What skills are employers looking for according to r/cscareerquestions?"

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Check your Reddit API credentials in the `.env` file
   - Verify that your Reddit account has the necessary permissions

2. **LLM Connection Issues**
   - Ensure Ollama is running with the llama3.2 model
   - Run `ollama pull llama3.2` if the model isn't already downloaded

3. **Event Loop Errors**
   - If you see "Already running asyncio in this thread" errors, restart the application

## Technical Details

### Project Structure

```
/trend_tracker_mcp
├── mcp_client/              # Client-side application
│   ├── llm_client/          # LLM integration
│   ├── mcp_session/         # MCP session management
│   └── main.py              # Client entry point
├── mcp_server/              # Server-side application
│   ├── reddit_scraper/      # Reddit API interaction
│   ├── server_impl/         # MCP server implementation
│   └── main.py              # Server entry point
└── README.md                # Project documentation
```

### Technologies Used

- **MCP**: Model Context Protocol for structured client-server communication
- **Ollama**: Local LLM integration with tool-calling capabilities
- **Reddit API**: OAuth-based data fetching from Reddit
- **AsyncIO**: Asynchronous I/O for improved performance
- **HTTPX**: Asynchronous HTTP client for API requests


