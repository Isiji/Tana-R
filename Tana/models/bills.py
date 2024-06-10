#!/usr/bin/python3
"""Bills class module for the bills"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

class Bills(BaseModel, Base):
    name = Column(String(128), nullable=False)
    submitted_date = Column(Date, nullable=False)
    first_reading = Column(Boolean, default=False)
    second_reading = Column(Boolean, default=False)
    third_reading = Column(Boolean, default=False)
    presidential_assent = Column(Boolean, default=False)
    commencement = Column(Boolean, default=False)
    documents = relationship("LegislationStages", back_populates="bill")