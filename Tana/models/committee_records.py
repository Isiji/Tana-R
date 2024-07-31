from sqlalchemy import Column, String, Integer, ForeignKey, Date, Text
from Tana.models.base_model import BaseModel, Base

class CommitteeRecord(Base, BaseModel):
    __tablename__ = 'committee_records'
    
    id = Column(Integer, primary_key=True)
    serial_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    title = Column(String(255), nullable=False)
    document = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    committee_id = Column(Integer, ForeignKey('committees.id'), nullable=False)
    
    def __init__(self, serial_number, date, title, document, recommendations, committee_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.serial_number = serial_number
        self.date = date
        self.title = title
        self.document = document
        self.recommendations = recommendations
        self.committee_id = committee_id
