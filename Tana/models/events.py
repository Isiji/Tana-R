from Tana.models.base_model import Base, BaseModel
from sqlalchemy import Column, Date, String, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from Tana.models.impactlevel import ImpactLevel

class Events(BaseModel, Base):
    __tablename__ = 'events'
    event_name = Column(String(128), nullable=False)
    impact_level = Column(Enum(ImpactLevel), nullable=False)
    event_owner = Column(String(128), nullable=False)
    event_location = Column(String(128), nullable=False)
    event_contact = Column(Integer, nullable=False)
    event_description = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)

    commitments = relationship("Commitments", back_populates="event")
    contributions = relationship("Contributions", back_populates="event")
    attendees = relationship("Attendees", back_populates="event")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
