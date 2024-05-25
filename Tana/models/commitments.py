#!/usr/bin/python3
"""Commitments class module for the commitments"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Commitments(BaseModel, Base):
    """This class defines the commitments model"""
    __tablename__ = 'commitments'
    commitment_title = Column(String(128), nullable=False)
    commitment_description = Column(String(128), nullable=False)
    commitment_date = Column(String(128), nullable=False)
    function_id = Column(Integer, ForeignKey('functions.id'))

    functions = relationship("Functions", back_populates="commitments")
    def __init__(self, *args, **kwargs):
        """Initialization of the commitments model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a commitment"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)