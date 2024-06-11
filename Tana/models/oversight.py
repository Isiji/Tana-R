#!/usr/bin/python3
"""Oversight class module for the oversight"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship, backref

class Oversight(BaseModel, Base):
    """This class defines the oversight model"""
    __tablename__ = 'oversight'
    id = Column(Integer, primary_key=True)
    type = Column(Enum("Primary", "Secondary"), nullable=False)
    document = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    
    
    def __init__(self, *args, **kwargs):
        """Initialization of the oversight model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """string represenation of a oversight"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)