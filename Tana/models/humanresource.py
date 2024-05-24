#!/usr/bin/python3
"""HumanResource class module for the humanresource"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class HumanResource(BaseModel, Base):
    """This class defines the humanresource model"""
    __tablename__ = 'humanresource'
    employee_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("users", back_populates="human_resources")
    ofiice_id = Column(Integer, ForeignKey('office.office_id'))
    job_title = Column(String(128), nullable=False)
    employment_date = Column(String(128), nullable=False)
    salary = Column(String(128), nullable=False)
    office = relationship("Office", back_populates="human_resources")
    def __init__(self, *args, **kwargs):
        """Initialization of the humanresource model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a humanresource"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)