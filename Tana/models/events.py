from Tana.models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from Tana.models.impactlevel import ImpactLevel

class Events(BaseModel, Base):
    __tablename__ = 'events'
    function_name = Column(String(128), nullable=False)
    impact_level = Column(Enum(ImpactLevel), nullable=False)
    function_owner = Column(String(128), nullable=False)
    function_location = Column(String(128), nullable=False)
    function_contact = Column(Integer, nullable=True)
    function_description = Column(Text, nullable=False)

    commitments = relationship("Commitments", back_populates="event")
    contributions = relationship("Contributions", back_populates="event")
    attendees = relationship("Attendees", back_populates="event")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
