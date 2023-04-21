from sqlalchemy import Column, Integer, String, Date, DateTime, func, event
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    birthday = Column(Date)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
