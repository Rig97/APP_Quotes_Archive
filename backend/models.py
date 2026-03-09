# backend/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # Relationship: a user can have many quotes
    quotes = relationship('Quote', back_populates='owner')




class Quote(Base):
    __tablename__ = 'quotes'


    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)          # The quote itself
    author = Column(String(150), nullable=False)  # Who said it
    category = Column(String(100))               # Topic or theme
    source = Column(String(255))                 # Book, speech, website
    date_added = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


    # Relationship: each quote belongs to one user
    owner = relationship('User', back_populates='quotes')
