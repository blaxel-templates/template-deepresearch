
FROM python:3.12-slim

ARG UV_VERSION="latest"
RUN apt update && apt install -y curl build-essential

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN curl -fsSL https://raw.githubusercontent.com/cploujoux/toolkit/main/install.sh | BINDIR=/bin sh
WORKDIR /blaxel

# Install the application dependencies.
COPY pyproject.toml /blaxel/pyproject.toml
COPY uv.lock /blaxel/uv.lock

COPY README.m[d] /blaxel/README.md
COPY LICENS[E] /blaxel/LICENSE
COPY src /blaxel/src

RUN uv sync --no-cache --no-dev

ENV PATH="/blaxel/.venv/bin:$PATH"

ENTRYPOINT ["bl","serve","--port","80","--module","agent.main","--remote"]
