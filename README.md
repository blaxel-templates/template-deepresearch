# Template DeepResearch

[![Build Status](https://github.com/blaxel-templates/template-deepresearch/actions/workflows/ci.yml/badge.svg)](https://github.com/blaxel-templates/template-deepresearch/actions)
[![PyPI](https://img.shields.io/pypi/v/template-deepresearch.svg)](https://pypi.org/project/template-deepresearch)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)
[![Python Versions](https://img.shields.io/pypi/pyversions/template-deepresearch.svg)]

A template for implementing a deep research agent using [LangGraph](https://github.com/langchain-ai/open_deep_research) and GPT-4. The agent:

- Generates multi-step research plans
- Executes web searches via [Tavily](https://app.tavily.com)
- Writes detailed, section-based reports
- Compiles final deliverables for web delivery
- Supports configurable depth and iterative refinement

## Table of Contents
1. [Features](#features)
2. [Demo](#demo)
3. [Installation](#installation)
4. [Usage](#usage)
   - [CLI](#cli)
   - [Server API](#server-api)
5. [Configuration](#configuration)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
8. [License](#license)

## Features

- Automatic research plan generation & execution
- Parallel processing of research sections
- Structured report output with citations
- Configurable search depth and recursion limits
- Easy deployment on [Blaxel](https://docs.blaxel.ai/Get-started)

## Demo

<!-- Embed demo GIF or asciinema here -->

## Installation

### Prerequisites

- Python 3.12+  
- [Blaxel CLI](https://docs.blaxel.ai/Get-started)  
- [Tavily API Key](https://app.tavily.com)

```bash
pip install template-deepresearch
```

Or clone and install locally:

```bash
git clone https://github.com/blaxel-templates/template-deepresearch.git
cd template-deepresearch
pip install -e .
```

## Usage

### CLI

Generate and execute a report:

```bash
template-deepresearch --input "Outline research on climate change" \
  --report-plan-depth 20 --recursion-limit 100
```

Start a local chat session:

```bash
bl chat --local template-deepresearch
```

### Server API

Run the FastAPI server:

```bash
uvicorn server.main:app --reload
```

Submit a request:

```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"input": "Research renewable energy trends", "report_plan_depth": 20}'
```

## Configuration

Copy the sample `.env` and update credentials:

```bash
cp .env-sample .env
```

| Variable         | Description               |
|------------------|---------------------------|
| TAVILY_API_KEY   | Tavily API credentials    |
| BLAXEL_API_KEY   | Blaxel CLI authentication |

## Project Structure

```
.
├── src/
│   ├── main.py          # CLI entrypoint
│   ├── agent.py         # Agent orchestration
│   ├── llmlogic.py      # LLM workflow logic
│   ├── prompts.py       # Prompt templates
│   ├── server/main.py   # FastAPI server
│   └── middleware.py    # Request middleware
├── tests/               # Unit tests
├── .env-sample          # Sample environment variables
└── README.md
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/foo`)
3. Commit your changes (`git commit -m "feat: add new feature"`)
4. Push to the branch (`git push origin feature/foo`)
5. Open a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT © 2025 Blaxel AI
