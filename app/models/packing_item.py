from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class PackingItem(Base):
    __tablename__ = "packing_items"

    id = Column(Integer, primary_key=True, index=True)

    item_name = Column(String(200), nullable=False)

    category = Column(String(100), nullable=True)

    is_packed = Column(Boolean, default=False)

    trip_id = Column(Integer, ForeignKey("trips.id"))

    trip = relationship("Trip", back_populates="packing_items")