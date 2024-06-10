#!/usr/bin/python3
"""PrimaryOversight class module for the primaryoversight"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import relationship, backref

class PrimaryOversight(BaseModel, Base):
    __tablename__ = 'primary_oversight'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    representation_id = Column(Integer, ForeignKey('representation.id'))
    document = Column(String, nullable=False)
    date_updated = Column(Date, nullable=False)
    
    user = relationship("Users", back_populates="primary_oversight")
    representation = relationship("Representation", back_populates="primary_oversight")
    
    def __init__(self, *args, **kwargs):
        """Initialization of the primaryoversight model"""
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        """string represenation of a primaryoversight"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)