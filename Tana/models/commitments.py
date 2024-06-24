from Tana.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

class Commitments(BaseModel, Base):
    __tablename__ = 'commitments'
    commitment_title = Column(String(128), nullable=False)
    commitment_description = Column(String(128), nullable=False)
    commitment_date = Column(Date, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'))

    event = relationship("Events", back_populates="commitments")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
