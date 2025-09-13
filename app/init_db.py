import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models import Base, Band, Venue, Gig

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_data():
    async with AsyncSessionLocal() as session:
        # Create bands
        band1 = Band(name="The Jazz Cats", description="A smooth jazz afternoon set.")
        band2 = Band(name="Blue Notes", description="Acoustic jazz ensemble.")
        band3 = Band(name="Funky Trio", description="Funky groovy set.")
        band4 = Band(name="Another Band", description="Extra performance.")

        # Create venues
        v1 = Venue(name="Main Stage", color="#e74c3c")
        v2 = Venue(name="Jazz Cafe", color="#3e1faf")
        v3 = Venue(name="Park Stage", color="#27ae60")
        v4 = Venue(name="Club", color="#f1c40f")

        session.add_all([band1, band2, band3, band4, v1, v2, v3, v4])
        await session.commit()

        # Create gigs
        gigs = [
            Gig(band_id=band1.id, venue_id=v1.id, start_time=datetime(2025, 9, 15, 14, 0), end_time=datetime(2025, 9, 15, 15, 0), description=band1.description),
            Gig(band_id=band2.id, venue_id=v2.id, start_time=datetime(2025, 9, 15, 14, 30), end_time=datetime(2025, 9, 15, 15, 30), description=band2.description),
            Gig(band_id=band3.id, venue_id=v3.id, start_time=datetime(2025, 9, 15, 14, 0), end_time=datetime(2025, 9, 15, 15, 0), description=band3.description),
            Gig(band_id=band4.id, venue_id=v4.id, start_time=datetime(2025, 9, 15, 14, 30), end_time=datetime(2025, 9, 15, 15, 30), description=band4.description),
        ]

        session.add_all(gigs)
        await session.commit()

async def main():
    await init_db()
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())
