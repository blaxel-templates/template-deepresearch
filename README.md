<p align="center">
  <img src="https://blaxel.ai/logo.png" alt="Blaxel" width="200"/>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.12+](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)

</div>

# Template DeepResearch Agent

A template implementation of a deep research agent using LangGraph & GPT-4. This agent performs comprehensive research on any given topic by:

1. Generating an initial research plan and outline
2. Breaking down the topic into logical sections
3. Performing targeted web searches using Tavil API for each section
4. Writing detailed section content based on search results
5. Compiling and refining the final report

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Server Locally](#running-the-server-locally)
- [Testing Your Agent](#testing-your-agent)
- [Deploying to Blaxel](#deploying-to-blaxel)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contribution](#contribution)
- [Support](#support)
- [License](#license)

## Features

- Interactive conversational interface
- Automated research planning and execution
- Parallel processing of research sections
- Web search integration via Tavil API
- Structured report generation with citations
- Configurable search depth and report formatting

## Quick Start

Clone the repository and install dependencies:

```bash
git clone https://github.com/blaxel-templates/template-deepresearch.git
cd template-deepresearch
uv sync
```

## Prerequisites

- Python: 3.12 or later
- [uv](https://github.com/astral-sh/uv)

## Installation

```bash
git clone https://github.com/blaxel-templates/template-deepresearch.git
cd template-deepresearch
uv sync
```

## Environment Variables

Create a `.env` file and define your credentials. Copy the sample file:

```bash
cp .env-sample .env
```

Update the following variables with your own credentials:

- `TAVILY_API_KEY`

## Running the Server Locally

Start the development server:

```bash
bl serve --hotreload
```

## Testing Your Agent

Run the agent template locally:

```bash
bl chat --local template-deepresearch
```

Or run with specific input:

```bash
bl run agent template-deepresearch --local --data '{"input": "What is the weather in Paris?"}'
```

## Deploying to Blaxel

Deploy your application to Blaxel:

```bash
bl deploy
```

This command uses your code and configuration files under the `blaxel` directory to deploy your application.

## API Reference

The agent exposes the following endpoints:

- **POST** `/agents/{agent_id}/run`: Run the agent with provided input
- **GET** `/agents/{agent_id}/info`: Get agent metadata and capabilities
- **GET** `/health`: Health check endpoint

For detailed API documentation, run the server and visit `/docs` endpoint.

## Project Structure

- **src/main.py** - Application entry point
- **src/agent/** - Configuration for chat agent, streams HTTP responses, and integrates conversational context
- **src/llmLogic.py** - Where the magic happens
- **src/prompts.py** - List of prompts given to agents
- **src/server/** - Server implementation and routing
- **middleware.py** - Define middleware for your API
- **error.py** - Handle error for requests
- **pyproject.toml** - UV package manager file
- **blaxel.toml** - Configuration file for deployment on Blaxel

## Examples

### Basic Conversation

```bash
bl chat --local template-deepresearch
```

### Weather Query

```bash
bl run agent template-deepresearch --local --data '{"input": "What is the weather like in San Francisco?"}'
```

## Troubleshooting

- Ensure Python 3.12+ is installed
- Verify network connectivity for API calls
- Confirm environment variables in `.env` file

## Contribution

Contributions are welcome! Here’s how you can contribute:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
git checkout -b feature/awesome-feature
```
3. **Commit** your changes:
   ```bash
git commit -am "Add awesome feature"
```
4. **Push** to the branch:
   ```bash
git push origin feature/awesome-feature
```
5. **Open** a Pull Request

## Support

If you need help with this template:

- Submit an issue on GitHub: https://github.com/blaxel-templates/template-deepresearch/issues
- Visit our [Blaxel Documentation](https://docs.blaxel.ai)
- Join our [Discord Community](https://discord.gg/G3NrzUPcHP)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
