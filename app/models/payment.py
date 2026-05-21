from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import mapped_column, relationship

from app.db.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = mapped_column(Integer, primary_key=True)

    order_id = mapped_column(ForeignKey("orders.id"))
    reference = mapped_column(String, unique=True)
    status = mapped_column(String, default="pending")

    amount = mapped_column(Numeric(10, 2))

    order = relationship("Order", back_populates="payment")
