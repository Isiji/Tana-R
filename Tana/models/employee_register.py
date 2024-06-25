#!/usr/bin/python3
""" employees should be able to register and time in and out of work"""

from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship, backref

class EmployeeRegister(BaseModel, Base):
    """This class defines the employee register model"""
    __tablename__ = 'employee_register'
    name = Column(String(255), nullable=False)
    time_in = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum("Present", "Absent", "Sick", "Leave"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("users", backref=backref("employee_registers", cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        """Initialization of the employee register model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string representation of an employee register"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)
