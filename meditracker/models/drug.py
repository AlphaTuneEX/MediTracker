from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base
from ..debug_function import ECHO, DEBUG

class Drug(Base):
    __tablename__ = "drugs"

    id = Column(
        Integer,
        primary_key = True
    )

    name = Column(
        String,
        nullable = False,
        unique = True
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable = False
    )

    dose = Column(
        Integer,
        nullable = False
    )

    unit = Column(
        String,
        default = "mg"
    )

    ingredient = relationship(
        "Ingredient"
    )

    def __repr__(self):
        return(
            f"<Drug {self.name} "
            f"{self.dose}{self.unit}>"
        )