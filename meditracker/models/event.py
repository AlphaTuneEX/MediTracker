from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base

class MedicationEvent(Base):
    __tablename__ = "events"

    id = Column(
        Integer,
        primary_key = True
    )

    time = Column(
        DateTime,
        nullable = False
    )

    treatment_id = Column(
        Integer,
        ForeignKey("treatments.id"),
        nullable = False
    )

    amount = Column(
        Integer,
        nullable = False,
        default = 1
    )

    note = Column(
        String
    )

    treatment = relationship(
        "Treatment"
    )

    event_type = Column(
        String,
        nullable = False,
        default = "medication"
    )

    def __repr__(self):
        return (
            f"<Event "
            f"{self.time} "
            f"x{self.amount}>"
        )