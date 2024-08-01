from sqlalchemy import Column, String, Integer, ForeignKey, Date, LargeBinary
from Tana.models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
class CommitteeRecord(Base, BaseModel):
    __tablename__ = 'committee_records'
    
    id = Column(Integer, primary_key=True)
    serial_number = Column(String(50), nullable=False)  # Updated to String
    date = Column(Date, nullable=False)
    title = Column(String(255), nullable=False)
    document = Column(LargeBinary(length=4294967295), nullable=True)  # Updated to LargeBinary
    recommendations = Column(LargeBinary(length=4294967295), nullable=True)  # Updated to LargeBinary
    committee_id = Column(Integer, ForeignKey('committees.id'), nullable=False)
    
    committee = relationship('Committee', back_populates='records')
    
    def __init__(self, serial_number, date, title, document, recommendations, committee_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial_number = serial_number
        self.date = date
        self.title = title
        self.document = document
        self.recommendations = recommendations
        self.committee_id = committee_id
