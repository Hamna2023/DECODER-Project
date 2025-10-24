from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app.models import SensorReading
from datetime import datetime
from pydantic import BaseModel
import pandas as pd

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-DECODER")

# Pydantic model for input
class SensorReadingIn(BaseModel):
    building_id: str
    sensor_id: str
    timestamp: datetime
    value: float


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Welcome to Mini-DECODER!"}


# POST /ingest
@app.post("/ingest")
def ingest_reading(reading: SensorReadingIn, db: Session = Depends(get_db)):
    new_reading = SensorReading(
        building_id=reading.building_id,
        sensor_id=reading.sensor_id,
        timestamp=reading.timestamp,
        value=reading.value
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return {"message": "Reading stored successfully!", "id": new_reading.id}


# GET /forecast
@app.get("/forecast/")
def get_forecast(
    building_id: str = Query(...),
    sensor_id: str = Query(...),
    db: Session = Depends(get_db)
):
    # Get all readings for that building + sensor
    readings = db.query(SensorReading).filter_by(
        building_id=building_id,
        sensor_id=sensor_id
    ).order_by(SensorReading.timestamp).all()

    if not readings:
        return {"message": "No data found for given building/sensor."}

    # Convert to DataFrame
    df = pd.DataFrame([{
        "timestamp": r.timestamp,
        "value": r.value
    } for r in readings])

    # Simple moving average forecast (last 3 values)
    last_values = df["value"].tail(3)
    avg = last_values.mean()

    # Simulate 3 future timestamps (1h apart)
    last_time = df["timestamp"].max()
    future_times = [last_time + pd.Timedelta(hours=i) for i in range(1, 4)]

    forecast_values = [avg] * 3  # same average repeated

    forecast_df = pd.DataFrame({
        "timestamp": future_times,
        "predicted_value": forecast_values
    })

    return forecast_df.to_dict(orient="records")
