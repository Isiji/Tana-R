#!/usr/bin/python3
"""users class module for the users"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from flask_login import UserMixin
from Tana.models.roles import UserRole

class users(BaseModel, Base, UserMixin):
    """This class defines the users model"""
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    phone = Column(Integer, nullable=False)
    ID_No = Column(Integer, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=False)
    profile_pic = Column(String(255), nullable=False)

    diaries = relationship("Diary", back_populates="user")
    human_resources = relationship("HumanResource", uselist=False, back_populates="user")
    tasks_assigned = relationship("Tasks", back_populates="assigned_by_user", foreign_keys="Tasks.assigned_by")
    tasks_assigned_to = relationship("Tasks", back_populates="assigned_to_user", foreign_keys="Tasks.assigned_to")
    reminders = relationship("Reminder", back_populates="user")
    offices = relationship("Offices", back_populates="users")

    def __init__(self, *args, **kwargs):
        """Initialization of the users model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation of a user"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
