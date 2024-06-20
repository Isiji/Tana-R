#!/usr/bin/python3
"""constituency class module for the constituency"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Constituency(BaseModel, Base):
    """This class defines the constituency model"""
    __tablename__ = 'constituencies'
    name = Column(String(128), nullable=False)
    wards = relationship("Ward", back_populates="constituency")

    def __init__(self, *args, **kwargs):
        """Initialization of the constituency model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """String representation of a constituency"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
