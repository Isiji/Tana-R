#!/usr/bin/python3
"""Subcounty class module for the subcounty"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Subcounty(BaseModel, Base):
    """This class defines the subcounty model"""
    __tablename__ = 'subcounties'
    name = Column(String(128), nullable=False)
    constituencies = relationship("Constituency", back_populates="subcounty")    
    def __init__(self, *args, **kwargs):
        """Initialization of the subcounty model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """string represenation of a subcounty"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)