#!/usr/bin/python3
"""Statements class module for the statements"""

from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Date, Enum, LargeBinary
from sqlalchemy.orm import relationship

class Statements(BaseModel, Base):
    """This class defines the statements model"""
    __tablename__ = 'statements'
    id = Column(Integer, primary_key=True)
    document = Column(LargeBinary(length=4294967295), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum("Pending", "Approved", "Rejected"), nullable=False)
    filename = Column(String(255), nullable=False)
    
    def __init__(self, document, date, status, *args, **kwargs):
        """Initialization of the statements model"""
        super().__init__(*args, **kwargs)
        self.document = document
        self.date = date
        self.status = status
        
    def __str__(self):
        """String representation of a statement"""
        return f"{self.__class__.__name__} (ID: {self.id}, Date: {self.date}, Status: {self.status})"
