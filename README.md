# Template DeepResearch

A template implementation of a deep research agent using LangGraph and GPT-4. This agent performs comprehensive research on any given topic by:

1. Generating an initial research plan and outline
2. Breaking down the topic into logical sections
3. Performing targeted web searches using Tavily for each section
4. Writing detailed section content based on search results
5. Compiling and refining the final report

The implementation uses LangGraph for orchestrating the research workflow, with parallel processing of sections for improved efficiency. It leverages GPT-4 for content generation and the Tavily search API for gathering relevant, up-to-date information from the web.

Key features:

- Automated research planning and execution
- Parallel processing of research sections
- Web search integration via Tavily
- Structured report generation with citations
- Configurable search depth and report formatting

Special thanks to:

- [MG](https://www.analyticsvidhya.com/blog/2025/02/build-your-own-deep-research-agent): Creating this agent and showing an amazing tutorial
- [Langchain](https://github.com/langchain-ai/open_deep_research/tree/main): Creating an awesome implementation of DeepResearch with langgraph
- [OpenAI](https://openai.com/index/introducing-deep-research/): Showing everyone this feature

## Prerequisites

- **Python:** 3.12 or later.
- **[UV](https://github.com/astral-sh/uv):** An extremely fast Python package and project manager, written in Rust.
- **[Blaxel CLI](https://docs.blaxel.ai/Get-started):** Ensure you have the Blaxel CLI installed. If not, install it globally:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/beamlit/toolkit/main/install.sh | BINDIR=$HOME/.local/bin sh
  ```
- **Blaxel login:** Login to Blaxel platform
  ```bash
    bl login YOUR-WORKSPACE
  ```

## Installation

- **Clone the repository and install the dependencies**:

  ```bash
  git clone https://github.com/beamlit/template-deepresearch.git
  cd template-deepresearch
  uv sync
  ```

- **Environment Variables:** Create a `.env` file with your configuration. You can begin by copying the sample file:

  ```bash
  cp .env-sample .env
  ```

  Then, update the following values with your own credentials:

  - [Tavily Api Key](https://app.tavily.com/home): `TAVILY_API_KEY`

## Running the Server Locally

Start the development server with hot reloading using the Blaxel CLI command:

```bash
bl serve --hotreload
```

_Note:_ This command starts the server and enables hot reload so that changes to the source code are automatically reflected.

## Testing your agent

```bash
bl chat --local template-deepresearch
```

_Note:_ This command starts a chat interface. Example question: Do a report of annual revenu for the last 10 years of NVIDIA

or

```
bl run agent template-deepresearch --local --data '{"input": "Do a report of annual revenu for the last 10 years of NVIDIA", "report_plan_depth": 20, "recursion_limit": 100 }'
```

## Deploying to Blaxel

When you are ready to deploy your application, run:

```bash
bl deploy
```

This command uses your code and the configuration files under the `.blaxel` directory to deploy your application.

## Project Structure

- **src/main.py** - This is your entrypoint
- **src/agent**
  - `/agent.py` - Configures the chat agent, streams HTTP responses, and integrates conversational context.
  - `/llmlogic.py` - Where the magic happens
  - `/prompts.py` - List of prompts given to agents
  - `/functions` - Functions to search the web with Tavily
- **src/server**
  - `/router.py` - Define routes for your API
  - `/middleware.py` - Define middleware for your API
  - `/error.py` - Handle error for Request
- **pyproject.toml** - UV package manager file.
- **blaxel.toml** - Configuration file for deployment on blaxel

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
