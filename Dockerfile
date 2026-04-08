FROM python:3.14

RUN mkdir -p ./usr/src/app/

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV PATH="/root/.local/bin:$PATH"

EXPOSE 8000

RUN uv sync

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]