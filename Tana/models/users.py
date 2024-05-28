#!/usr/bin/python3
"""users class module for the users"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Enum
from flask_login import UserMixin

class users(BaseModel, Base, UserMixin):
    """This class defines the users model"""
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    ID_No = Column(String(128), nullable=False)
    role = Column(Enum('admin', 'employee'), nullable=False)
    profile_pic = Column(String(255), nullable=False)

    diaries = relationship("Diary", back_populates="user")
    human_resources = relationship("HumanResources", uselist=False, back_populates="user")
    attendance = relationship("Attendance", back_populates="user")
    documents = relationship("Documents", back_populates="user")
    tasks_assigned = relationship("Tasks", back_populates="assigned_by")
    tasks_assigned_to = relationship("Tasks", back_populates="assigned_to")
    def __init__(self, *args, **kwargs):
        """Initialization of the users model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a user"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
    


