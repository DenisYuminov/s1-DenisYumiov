from sqlalchemy import Column, Integer, String, MetaData

from db import Base

metadata = MetaData()
class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)
    metadata = metadata