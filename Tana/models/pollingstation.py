#!/usr/bin/python3
"""PollingStation class module for the polling station"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class PollingStation(BaseModel, Base):
    __tablename__ = 'polling_stations'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    ward_id = Column(Integer, ForeignKey('wards.id'), nullable=False)
    ward = relationship("Ward", back_populates="polling_stations")

    def __init__(self, *args, **kwargs):
        """Initialization of the polling station model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """String representation of a polling station"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
