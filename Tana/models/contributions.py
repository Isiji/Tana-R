#!/usr/bin/python3
"""Contributions class module for the contributions"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Contributions(BaseModel, Base):
    """This class defines the contributions model"""
    __tablename__ = 'contributions'
    contribution_title = Column(String(128), nullable=False)
    contribution_description = Column(String(128), nullable=False)
    contribution_date = Column(Date, nullable=False)
    function_id = Column(Integer, ForeignKey('functions.id'))

    functions = relationship("Functions", back_populates="contributions")
    def __init__(self, *args, **kwargs):
        """Initialization of the contributions model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a contribution"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)