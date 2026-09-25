from fastapi import FastAPI
import models
from database import engine

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevShowcase API")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à DevShowcase API! O banco de dados foi criado."}