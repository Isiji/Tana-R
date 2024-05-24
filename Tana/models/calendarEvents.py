#!/usr/bin/python3
"""CalendarEvents class module for the calendarEvents"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class CalendarEvents(BaseModel, Base):
    """This class defines the calendarEvents model"""
    __tablename__ = 'calendarEvents'
    event_title = Column(String(128), nullable=False)
    event_description = Column(String(128), nullable=False)
    event_start_date = Column(String(128), nullable=False)
    event_end_date = Column(String(128), nullable=False)
    event_location = Column(String(128), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("users", back_populates="calendarEvents")
    def __init__(self, *args, **kwargs):
        """Initialization of the calendarEvents model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a calendarEvents"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)