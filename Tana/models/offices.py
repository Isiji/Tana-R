#!/usr/bin/python3
"""Users class for the users"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class Offices(BaseModel, Base, UserMixin):
    """This class defines the users model"""
    __tablename__ = 'offices'
    office_name = Column(String(128), nullable=False)
    office_location = Column(String(128), nullable=False)
    office_description = Column(String(128), nullable=False)
    office_contact = Column(String(128), nullable=True)
    def __init__(self, *args, **kwargs):
        """Initialization of the users model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a user"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)