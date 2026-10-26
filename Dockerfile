FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --no-install-project

# Bake extensions into the image so startup needs no network
COPY install_extensions.py ./
RUN uv run python install_extensions.py

COPY server.py ./
EXPOSE 9494
CMD ["uv", "run", "python", "server.py"]
