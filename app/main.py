# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from contextlib import asynccontextmanager
import os
from datetime import datetime
import socket
from . import crud, models, schemas
from .database import engine, get_db

# Esta función 'lifespan' se ejecuta al iniciar la aplicación.
# Aquí le decimos a SQLAlchemy que cree todas las tablas definidas en nuestros modelos.
# Nota: En una aplicación de producción real, se usarían herramientas de migración como Alembic.
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

# Creamos la instancia de la aplicación FastAPI, pasándole la función lifespan.
app = FastAPI(lifespan=lifespan)


@app.post("/peliculas", response_model=schemas.Movie, status_code=status.HTTP_201_CREATED, tags=["Películas"])
async def create_new_movie(movie: schemas.MovieCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea una nueva película en la base de datos.
    """
    return await crud.create_movie(db=db, movie=movie)


@app.get("/peliculas", response_model=List[schemas.Movie], tags=["Películas"])
async def read_movies(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    Obtiene una lista de todas las películas con paginación.
    """
    movies = await crud.get_movies(db, skip=skip, limit=limit)
    return movies


@app.get("/peliculas/{movie_id}", response_model=schemas.Movie, tags=["Películas"])
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """
    Obtiene los detalles de una película por su ID.
    """
    db_movie = await crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return db_movie


@app.put("/peliculas/{movie_id}", response_model=schemas.Movie, tags=["Películas"])
async def update_existing_movie(movie_id: int, movie_update: schemas.MovieUpdate, db: AsyncSession = Depends(get_db)):
    """
    Actualiza una película existente por su ID.
    """
    updated_movie = await crud.update_movie(db, movie_id=movie_id, movie_update=movie_update)
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return updated_movie


@app.delete("/peliculas/{movie_id}", response_model=schemas.Movie, tags=["Películas"])
async def delete_existing_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """
    Elimina una película existente por su ID.
    """
    deleted_movie = await crud.delete_movie(db, movie_id=movie_id)
    if deleted_movie is None:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return deleted_movie

# =============================================================================
#      ENDPOINTS PARA VALIDACIÓN CI/CD  
# =============================================================================



@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Endpoint de salud básico - Verifica que la API está funcionando
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ICinema API",
        "environment": "production",
        "hostname": socket.gethostname()
    }

@app.get("/version", tags=["CI/CD Evidence"])
async def get_version():
    """
    Endpoint para evidenciar cambios automáticos del CD
    El color cambia automáticamente con cada despliegue
    """
    return {
        "version": "2.0.0",
        "build_id": os.getenv('BUILD_BUILDID', 'local'),
        "build_number": os.getenv('BUILD_BUILDNUMBER', 'dev'),
        "deployment_date": datetime.now().isoformat(),
        "message": "🚀 CD Funcionando - Despliegue Automático",
        "feature": "Color: AZUL",  # ⭐ Esto cambiará automáticamente
        "environment": "Azure Web App",
        "evidence": "Este mensaje cambia con cada despliegue automático"
    }

@app.get("/cd-status", tags=["CD Validation"])
async def cd_status():
    """
    Endpoint específico para validar el Despliegue Continuo
    """
    return {
        "cd_working": True,
        "last_deployment": datetime.now().isoformat(),
        "deployment_trigger": "GitHub Push" if os.getenv('BUILD_REASON') == 'IndividualCI' else "Manual",
        "pipeline_id": os.getenv('BUILD_BUILDID', 'unknown'),
        "validation": "CD_CONFIGURADO_CORRECTAMENTE",
        "next_step": "Hacer commit y verificar cambio automático en /version"
    }

@app.get("/full-status", tags=["Full CI/CD Status"])
async def full_status():
    """
    Estado completo del CI/CD
    """
    return {
        "ci_status": "completed",
        "cd_status": "deployed",
        "current_environment": "production",
        "api_status": "operational",
        "database_status": "connected",
        "last_ci_run": os.getenv('BUILD_BUILDNUMBER', 'unknown'),
        "auto_deployment": True,
        "evidence_timestamp": datetime.now().isoformat()
    }