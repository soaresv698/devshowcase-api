from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Tabela Associativa para o relacionamento N:N (Project <-> Technology)
project_technology_association = Table(
    'project_technology',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('technology_id', Integer, ForeignKey('technologies.id'))
)

# 1. Entidade Profile
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    bio = Column(String)

    # Relacionamento 1:N com Project
    projects = relationship("Project", back_populates="owner")

# 2. Entidade Project
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    url = Column(String)
    profile_id = Column(Integer, ForeignKey("profiles.id")) # Chave estrangeira

    # Relacionamentos
    owner = relationship("Profile", back_populates="projects")
    feedbacks = relationship("Feedback", back_populates="project")
    # Relacionamento N:N com Technology
    technologies = relationship("Technology", secondary=project_technology_association, back_populates="projects")

# 3. Entidade Feedback
class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id")) # Chave estrangeira

    # Relacionamento
    project = relationship("Project", back_populates="feedbacks")

# 4. Entidade Technology
class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Relacionamento N:N com Project
    projects = relationship("Project", secondary=project_technology_association, back_populates="technologies")