from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# SQLite async database URL
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # set to False to disable SQL logging
    future=True,
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency for injecting session into FastAPI routes
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
