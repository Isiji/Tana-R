#!/usr/bin/python3
"""Village class module for the village"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Village(BaseModel, Base):
    __tablename__ = 'villages'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    ward_id = Column(Integer, ForeignKey('wards.id'))
    ward = relationship("Ward", back_populates="villages")