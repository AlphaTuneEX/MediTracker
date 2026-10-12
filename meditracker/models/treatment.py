from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from ..database import Base
from ..debug_function import ECHO

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(
        Integer,
        primary_key = True
    )

    name = Column(
        String,
        nullable = False
    )

    drug_id = Column(
        Integer,
        ForeignKey("drugs.id"),
        nullable = False
    )

    interval_hours = Column(
        Integer,
        nullable = False
    )


    start_date = Column(
        Date
    )


    end_date = Column(
        Date
    )


    drug = relationship(
        "Drug"
    )


    def __repr__(self):
        return (
            f"<Treatment {self.name} "
            f"{self.interval_hours}h>"
        )