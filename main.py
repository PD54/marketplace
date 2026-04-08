from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home() -> str:
    return "This is the homepage."
