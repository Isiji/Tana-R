#!/usr/bin/python3
"""Attendees class for the attendees"""

from Tana.models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Attendees(BaseModel, Base):
    """This class defines the attendees model"""
    __tablename__ = 'attendees'
    attendee_name = Column(String(128), nullable=False)
    attendee_email = Column(String(128), nullable=False)
    attendee_phone = Column(Integer, nullable=False)
    function_id = Column(Integer, ForeignKey('functions.id'), nullable=False)

    functions = relationship("Functions", back_populates="attendees")

    def __init__(self, *args, **kwargs):
        """Initialization of the attendees model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation of an attendee"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
