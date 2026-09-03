from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True) 
    email = Column(String, unique=True, nullable=False)
    height_cm = Column(Float, nullable=True)
    body_build = Column(String, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)

    # Establish relationships
    items = relationship("ClothingItem", back_populates="user", cascade="all, delete-orphan")
    outfits = relationship("Outfit", back_populates="user", cascade="all, delete-orphan")


class ClothingItem(Base):
    __tablename__ = "clothing_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    s3_url = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="items")
    labels = relationship("ItemLabel", back_populates="item", uselist=False, cascade="all, delete-orphan")


class ItemLabel(Base):
    __tablename__ = "item_labels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("clothing_items.id", ondelete="CASCADE"), unique=True, nullable=False)
    category = Column(String, nullable=False)  
    color = Column(String, nullable=False)     
    fit = Column(String, nullable=True)        
    tags = Column(ARRAY(String), default=[])   

    item = relationship("ClothingItem", back_populates="labels")


class Outfit(Base):
    __tablename__ = "outfits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    aesthetic = Column(String, nullable=False)        
    weather_summary = Column(String, nullable=True)   
    item_ids = Column(ARRAY(Integer), nullable=False) 
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="outfits")