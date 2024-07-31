#!/usr/bin/python3
"""SecondaryOversight class module for the secondaryoversight"""
from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, LargeBinary
from sqlalchemy.orm import relationship, backref


class SecondaryOversight(BaseModel, Base):
    __tablename__ = 'secondary_oversight'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    OAG_Report = Column(LargeBinary(length=4294967295), nullable=False)
    date_updated = Column(Date, nullable=False)
    Ground_report = Column(String(1000), nullable=False)
    status = Column(Boolean, default=False)
    
    def __init__(self, *args, **kwargs):
        """Initialization of the secondary oversight model"""
        super().__init__(*args, **kwargs)
