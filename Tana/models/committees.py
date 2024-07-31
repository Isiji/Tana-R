from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from Tana.models.base_model import BaseModel, Base

class Committee(Base, BaseModel):
    __tablename__ = 'committees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    records = relationship('CommitteeRecord', backref='committee', lazy=True)
    
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
