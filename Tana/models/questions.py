#!/usr/bin/python3
"""Questions class module for the questions, should be similar to the oversight class module for the oversight and a place to add the files for the questions"""

from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum, LargeBinary
from sqlalchemy.orm import relationship, backref

class Questions(BaseModel, Base):
    """This class defines the questions model"""
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    document = Column(LargeBinary, nullable=False)
    date = Column(Date, nullable=False)
    status = Column(Enum("Pending", "Approved", "Rejected"), nullable=False)        
    def __init__(self, *args, **kwargs):
        """Initialization of the questions model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """string represenation of a questions"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)