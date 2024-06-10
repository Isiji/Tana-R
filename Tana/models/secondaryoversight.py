#!/usr/bin/python3
"""SecondaryOversight class module for the secondaryoversight"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship, backref


class SecondaryOversight(BaseModel, Base):
    __tablename__ = 'secondary_oversight'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    document = Column(String, nullable=False)
    date_updated = Column(Date, nullable=False)
    status = Column(Boolean, default=False)
    
    user = relationship("Users", back_populates="secondary_oversight")