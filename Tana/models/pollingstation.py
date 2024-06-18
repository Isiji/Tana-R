#!/usr/bin/python3
"""PollingStation class module for the polling station"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class PollingStation(BaseModel, Base):
    __tablename__ = 'polling_stations'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    village_id = Column(Integer, ForeignKey('villages.id'))
    village = relationship("Village", back_populates="polling_stations")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    