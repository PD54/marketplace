FROM python:3.14

WORKDIR /usr/src/app/

COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /uvx /bin/

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

COPY pyproject.toml uv.lock .

RUN uv sync

COPY . .

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]