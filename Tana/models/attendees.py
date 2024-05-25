#!/usr/bin/python3
"""Attendees class module for the attendees"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Attendees(BaseModel, Base):
    """This class defines the attendees model"""
    __tablename__ = 'attendees'
    attendee_name = Column(String(128), nullable=False)
    attendee_email = Column(String(128), nullable=True)
    attendee_phone = Column(String(128), nullable=False)
    function_id = Column(Integer, ForeignKey('functions.id'))

    functions = relationship("Functions", back_populates="attendees")
    def __init__(self, *args, **kwargs):
        """Initialization of the attendees model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of an attendee"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)