from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

engine = create_async_engine(db_url)

SessionMaker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with SessionMaker() as db:
        try:
            yield db

        except Exception as e:
            await db.rollback()
            print(f"Error occurred: {e}")
            raise

        finally:
            await db.close()