#!/usr/bin/python3
"""LegislationStages class module for the legislationstages"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum, LargeBinary
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

class LegislationStages(BaseModel, Base):
    """This class defines the legislationstages model"""
    __tablename__ = 'legislationstages'
    stage = Column(Enum("First Reading", "Second Reading", "Third Reading", "Presidential Assent", "Commencement"), nullable=False)
    document = Column(LargeBinary, nullable=False)
    bill_id = Column(Integer, ForeignKey('bills.id'))
    
    bill = relationship("Bills", back_populates="documents")
    
    def __init__(self, *args, **kwargs):
        """Initialization of the legislationstages model"""
        super().__init__(*args, **kwargs)

    def __str__(self):
        """string represenation of a legislationstages"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)