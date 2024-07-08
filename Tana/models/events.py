from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from Tana.models.base_model import BaseModel, Base
from Tana.models.impactlevel import ImpactLevel

class Events(BaseModel, Base):
    __tablename__ = 'events'
    event_name = Column(String(128), nullable=False)
    impact_level = Column(Enum(ImpactLevel), nullable=False)
    event_owner = Column(String(128), nullable=False)
    event_location = Column(String(128), nullable=False)
    event_contact = Column(Integer, nullable=False)  # Changed to String
    event_description = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    polling_station_id = Column(Integer, ForeignKey('polling_stations.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    polling_station = relationship("PollingStation", back_populates="events")
    commitments = relationship("Commitments", back_populates="event")
    contributions = relationship("Contributions", back_populates="event")
    attendees = relationship("Attendees", back_populates="event")
    user = relationship("users", back_populates="events")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
