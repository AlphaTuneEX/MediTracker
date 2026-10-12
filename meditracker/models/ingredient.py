from sqlalchemy import Integer, String, Column

from ..database import Base

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(
        Integer,
        primary_key = True
    )

    name = Column(
        String,
        unique = True,
        nullable = False
    )

    category = Column(
        String
    )

    maximum_dose = Column(
        Integer
    )

    unit = Column(
        String,
        default = "mg"
    )

    def __repr__(self):
        return(
            f"<Ingredient {self.name}>"
        )