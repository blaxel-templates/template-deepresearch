# Blaxel Deep Research Agent

<p align="center">
  <img src="https://blaxel.ai/logo.png" alt="Blaxel" width="200"/>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-powered-brightgreen.svg)](https://github.com/langchain-ai/langgraph)
[![Tavily](https://img.shields.io/badge/Tavily-research-orange.svg)](https://tavily.com/)

</div>

A template implementation of a comprehensive deep research agent using LangGraph and GPT-4. This agent performs thorough research on any given topic by orchestrating multiple research phases, gathering information from multiple sources, and compiling detailed reports with citations and structured analysis.

## 📑 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Running Locally](#running-the-server-locally)
  - [Testing](#testing-your-agent)
  - [Deployment](#deploying-to-blaxel)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## ✨ Features

- Comprehensive multi-phase research methodology
- Automated research planning and outline generation
- Parallel processing of research sections for efficiency
- Web search integration via Tavily for up-to-date information
- Structured report generation with proper citations
- Configurable search depth and report formatting
- Built on LangGraph for sophisticated workflow orchestration
- Easy deployment and integration with Blaxel platform

## 🚀 Quick Start

For those who want to get up and running quickly:

```bash
# Clone the repository
git clone https://github.com/blaxel-ai/template-deepresearch.git

# Navigate to the project directory
cd template-deepresearch

# Install dependencies
uv sync

# Set up your Tavily API key
cp .env-sample .env
# Edit .env and add your TAVILY_API_KEY

# Start the server
bl serve --hotreload

# In another terminal, test the agent
bl chat --local template-deepresearch
```

## 📋 Prerequisites

- **Python:** 3.12 or later
- **[UV](https://github.com/astral-sh/uv):** An extremely fast Python package and project manager, written in Rust
- **[Tavily API Key](https://app.tavily.com/home):** Required for web search functionality
- **Blaxel Platform Setup:** Complete Blaxel setup by following the [quickstart guide](https://docs.blaxel.ai/Get-started#quickstart)
  - **[Blaxel CLI](https://docs.blaxel.ai/Get-started):** Ensure you have the Blaxel CLI installed. If not, install it globally:
    ```bash
    curl -fsSL https://raw.githubusercontent.com/blaxel-ai/toolkit/main/install.sh | BINDIR=/usr/local/bin sudo -E sh
    ```
  - **Blaxel login:** Login to Blaxel platform
    ```bash
    bl login YOUR-WORKSPACE
    ```

## 💻 Installation

**Clone the repository and install dependencies:**

```bash
git clone https://github.com/blaxel-ai/template-deepresearch.git
cd template-deepresearch
uv sync
```

**Set up environment variables:**

```bash
cp .env-sample .env
```

Then update the following values with your own credentials:
- **Tavily API Key**: `TAVILY_API_KEY`

## 🔧 Usage

### Running the Server Locally

Start the development server with hot reloading:

```bash
bl serve --hotreload
```

_Note:_ This command starts the server and enables hot reload so that changes to the source code are automatically reflected.

### Testing your agent

You can test your deep research agent using the chat interface:

```bash
bl chat --local template-deepresearch
```

Example research query: "Do a report of annual revenue for the last 10 years of NVIDIA"

Or run it directly with specific parameters:

```bash
bl run agent template-deepresearch --local --data '{"input": "Do a report of annual revenue for the last 10 years of NVIDIA", "report_plan_depth": 20, "recursion_limit": 100}'
```

### Deploying to Blaxel

When you are ready to deploy your application:

```bash
bl deploy
```

This command uses your code and the configuration files under the `.blaxel` directory to deploy your application.

## 📁 Project Structure

- **src/main.py** - Application entry point
- **src/agent/** - Core research agent implementation
  - **agent.py** - Main agent configuration and HTTP response streaming
  - **llmlogic.py** - Research workflow logic and LangGraph implementation
  - **prompts.py** - Research prompts and templates
- **src/server/** - Server implementation and routing
  - **router.py** - API route definitions
  - **middleware.py** - Request/response middleware
  - **error.py** - Error handling utilities
- **pyproject.toml** - UV package manager configuration
- **blaxel.toml** - Blaxel deployment configuration
- **.env-sample** - Environment variables template

## ❓ Troubleshooting

### Common Issues

1. **Blaxel Platform Issues**:
   - Ensure you're logged in to your workspace: `bl login MY-WORKSPACE`
   - Verify models are available: `bl get models`
   - Check that functions exist: `bl get functions`

2. **Tavily API Issues**:
   - Ensure your Tavily API key is valid and active
   - Check API usage limits and quotas
   - Verify network connectivity to Tavily services

3. **Research Depth Configuration**:
   - Adjust `report_plan_depth` for more detailed outlines
   - Increase `recursion_limit` for complex research topics
   - Monitor processing time for large research projects

4. **Memory and Performance**:
   - Large research topics may require significant processing time
   - Consider breaking down extremely broad topics
   - Monitor system resources during parallel processing

5. **Citation and Source Quality**:
   - Review search terms and refine for better results
   - Check date ranges for time-sensitive research
   - Verify source credibility in generated reports

For more help, please [submit an issue](https://github.com/blaxel-templates/template-deepresearch/issues) on GitHub.

## 👥 Contributing

Contributions are welcome! Here's how you can contribute:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** your changes:
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Submit** a Pull Request

Please make sure to update tests as appropriate and follow the code style of the project.

## 🆘 Support

If you need help with this template:

- [Submit an issue](https://github.com/blaxel-templates/template-deepresearch/issues) for bug reports or feature requests
- Visit the [Blaxel Documentation](https://docs.blaxel.ai) for platform guidance
- Check the [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) for workflow framework help
- Join our [Discord Community](https://discord.gg/G3NqzUPcHP) for real-time assistance

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgements

Special thanks to:

- **[MG](https://www.analyticsvidhya.com/blog/2025/02/build-your-own-deep-research-agent)**: Creating this agent and showing an amazing tutorial
- **[Langchain](https://github.com/langchain-ai/open_deep_research/tree/main)**: Creating an awesome implementation of DeepResearch with LangGraph
- **[OpenAI](https://openai.com/index/introducing-deep-research/)**: Showing everyone this feature
