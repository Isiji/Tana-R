#!/usr/bin/python3
"""Statements class module for the statements, should be similar to the oversight class module for the oversight and a place to add the files for the statements"""

from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum, LargeBinary
from sqlalchemy.orm import relationship, backref

class Statements(BaseModel, Base):
    """This class defines the statements model"""
    __tablename__ = 'statements'
    id = Column(Integer, primary_key=True)
    document = Column(LargeBinary, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum("Pending", "Approved", "Rejected"), nullable=False)
        
    def __init__(self, *args, **kwargs):
        """Initialization of the statements model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """string represenation of a statements"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)