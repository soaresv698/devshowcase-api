from fastapi import FastAPI

app = FastAPI(title="DevShowcase API")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à DevShowcase API!"}