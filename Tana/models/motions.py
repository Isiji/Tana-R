#!/usr/bin/python3
"""Motions class module for the motions, similar to the oversight class module for the oversight."""

from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum, LargeBinary
from sqlalchemy.orm import relationship, backref

class Motions(BaseModel, Base):
    """This class defines the motions model"""
    __tablename__ = 'motions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    document = Column(LargeBinary, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum("Pending", "Approved", "Rejected"), nullable=False)
        
    def __init__(self, *args, **kwargs):
        """Initialization of the motions model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """String representation of a motion"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
