from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base
from datetime import datetime

class SensorData(Base):
    __tablename__ = "sensor_data"  

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(String, index=True)
    meter_type = Column(String, index=True)
    timestamp = Column(DateTime)
    value = Column(Float)
