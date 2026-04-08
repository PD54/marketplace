FROM python:3.14

WORKDIR /usr/src/app/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV UV_PROJECT_ENVIRONMENT="/usr/local/" \
    PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock .

RUN uv sync

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]