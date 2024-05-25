#!/usr/bin/python3
"""Functions class for the functions"""

from Tana.models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from Tana.models.funcategory import FunctionCategory
from Tana.models.impactlevel import ImpactLevel

class Functions(BaseModel, Base):
    """This class defines the functions model"""
    __tablename__ = 'functions'
    function_name = Column(String(128), nullable=False)
    category = Column(Enum(FunctionCategory), nullable=False)
    impact_level = Column(Enum(ImpactLevel), nullable=False)
    function_owner = Column(String(128), nullable=False)
    function_location = Column(String(128), nullable=False)
    function_contact = Column(String(128), nullable=True)
    function_description = Column(Text, nullable=False)

    commitments = relationship("Commitments", back_populates="functions")
    contributions = relationship("Contributions", back_populates="functions")
    
    def __init__(self, *args, **kwargs):
        """Initialization of the functions model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a user"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)