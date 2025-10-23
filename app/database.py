from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
#from dotenv import load_dotenv
import ssl
#load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Detectar si estamos en Azure
def is_azure_environment():
    return DATABASE_URL and "postgres.database.azure.com" in DATABASE_URL

if is_azure_environment():
    # Configuración para Azure PostgreSQL con SSL
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,
        connect_args={
            "ssl": ssl.create_default_context(cafile="/etc/ssl/certs/ca-certificates.crt")
        }
    )
else:
    # Configuración Local
    engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
