from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base
from datetime import datetime

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(String, index=True)
    sensor_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    value = Column(Float)
