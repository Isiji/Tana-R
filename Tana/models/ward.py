#!/usr/bin/python3
"""Ward class module for the ward"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Ward(BaseModel, Base):
    """This class defines the ward model"""
    __tablename__ = 'ward'
    name = Column(String(128), nullable=False, unique=True)
    constituency_id = Column(Integer, ForeignKey('constituencies.id'))
    constituency = relationship("Constituency", back_populates="wards")
    villages = relationship("Village", back_populates="ward")
    def __init__(self, *args, **kwargs):
        """Initialization of the ward model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """string represenation of a ward"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)