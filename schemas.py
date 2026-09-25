from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

# ==========================================
# DTOs de Tecnologia
# ==========================================
class TechnologyBase(BaseModel):
    # Field(min_length=1) garante que o nome não seja enviado vazio
    name: str = Field(..., min_length=1, description="O nome da tecnologia é obrigatório.")

class TechnologyCreate(TechnologyBase):
    pass

class TechnologyResponse(TechnologyBase):
    id: int

    class Config:
        from_attributes = True # Permite que o Pydantic leia os dados do banco (SQLAlchemy)

# ==========================================
# DTOs de Projeto
# ==========================================
class ProjectBase(BaseModel):
    # Validação exigida pela tarefa: Títulos não vazios
    title: str = Field(..., min_length=1, description="O título não pode ser vazio.")
    description: Optional[str] = None
    # Validação exigida pela tarefa: URLs válidas
    url: Optional[HttpUrl] = None 

class ProjectCreate(ProjectBase):
    profile_id: int # Para criar um projeto, precisamos saber de qual perfil ele é

class ProjectResponse(ProjectBase):
    id: int
    profile_id: int
    technologies: List[TechnologyResponse] = []

    class Config:
        from_attributes = True

# ==========================================
# DTOs de Perfil
# ==========================================
class ProfileBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: str
    bio: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileResponse(ProfileBase):
    id: int
    projects: List[ProjectResponse] = [] # Ao buscar um perfil, trazemos os projetos dele

    class Config:
        from_attributes = True