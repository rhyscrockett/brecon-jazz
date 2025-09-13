from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Band(Base):
    __tablename__ = "bands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)

    gigs = relationship("Gig", back_populates="band")

class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    color = Column(String(7))  # Hex color like #e74c3c

    gigs = relationship("Gig", back_populates="venue")

class Gig(Base):
    __tablename__ = "gigs"
    id = Column(Integer, primary_key=True, index=True)
    band_id = Column(Integer, ForeignKey("bands.id"), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    description = Column(Text)

    band = relationship("Band", back_populates="gigs")
    venue = relationship("Venue", back_populates="gigs")
