#!/usr/bin/python3
"""Reminder class module for the reminder"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Reminder(BaseModel, Base):
    """This class defines the reminder model"""
    __tablename__ = 'reminder'
    reminder_title = Column(String(128), nullable=False)
    reminder_description = Column(String(128), nullable=False)
    reminder_date = Column(String(128), nullable=False)
    reminder_time = Column(String(128), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("users", back_populates="reminder")
    def __init__(self, *args, **kwargs):
        """Initialization of the reminder model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a reminder"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)