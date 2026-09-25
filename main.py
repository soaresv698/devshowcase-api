from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importando nossos arquivos
import models
import schemas
from database import engine, get_db

# Cria as tabelas no banco de dados automaticamente
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevShowcase API")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à DevShowcase API! A API está online."}

# ==========================================
# Endpoints de Profiles (Perfis)
# ==========================================

@app.post("/api/profiles", response_model=schemas.ProfileResponse, status_code=201)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    # Verifica se o email já existe para evitar erro no banco
    db_profile = db.query(models.Profile).filter(models.Profile.email == profile.email).first()
    if db_profile:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    
    # Cria o modelo, salva no banco, commita e atualiza a variável com o ID gerado
    new_profile = models.Profile(**profile.model_dump())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@app.get("/api/profiles/{id}", response_model=schemas.ProfileResponse)
def get_profile(id: int, db: Session = Depends(get_db)):
    # Busca o perfil pelo ID
    db_profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return db_profile

# ==========================================
# Endpoints de Technologies (Tecnologias)
# ==========================================

@app.post("/api/technologies", response_model=schemas.TechnologyResponse, status_code=201)
def create_technology(tech: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    # Verifica se a tecnologia já existe
    db_tech = db.query(models.Technology).filter(models.Technology.name == tech.name).first()
    if db_tech:
        raise HTTPException(status_code=400, detail="Tecnologia já cadastrada.")
    
    new_tech = models.Technology(**tech.model_dump())
    db.add(new_tech)
    db.commit()
    db.refresh(new_tech)
    return new_tech

@app.get("/api/technologies", response_model=List[schemas.TechnologyResponse])
def list_technologies(db: Session = Depends(get_db)):
    # Retorna todas as tecnologias cadastradas
    return db.query(models.Technology).all()

# ==========================================
# Endpoints de Projects (Projetos)
# ==========================================

@app.post("/api/projects", response_model=schemas.ProjectResponse, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    # Verifica se o dono do projeto (profile_id) realmente existe
    db_profile = db.query(models.Profile).filter(models.Profile.id == project.profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil associado não encontrado.")

    # A URL vem como um objeto HttpUrl do Pydantic, precisamos converter para string para salvar no banco SQLite
    project_data = project.model_dump()
    if project_data.get("url"):
        project_data["url"] = str(project_data["url"])
    
    new_project = models.Project(**project_data)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@app.get("/api/projects", response_model=List[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    # Retorna todos os projetos
    return db.query(models.Project).all()