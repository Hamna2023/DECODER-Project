from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import pandas as pd

from app.database import Base, engine, SessionLocal
from app.models import SensorData

# Create all tables (ensures schema is synced)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-DECODER API")

# ---------------------- SCHEMA ----------------------
class SensorReadingIn(BaseModel):
    building_id: str
    meter_type: str
    timestamp: Optional[datetime] = None
    value: float

# ---------------------- DEPENDENCY ----------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- ROOT ----------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Mini-DECODER API"}

# ---------------------- INGEST ----------------------
@app.post("/ingest", status_code=201)
def ingest_reading(reading: SensorReadingIn, db: Session = Depends(get_db)):
    """Store a new sensor reading in the database."""
    try:
        timestamp = reading.timestamp or datetime.utcnow()
        new_record = SensorData(
            building_id=reading.building_id,
            meter_type=reading.meter_type,
            timestamp=timestamp,
            value=reading.value
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return {"message": "Reading stored successfully!", "id": new_record.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------- FORECAST ----------------------
@app.get("/forecast/")
def get_forecast(
    building_id: str = Query(..., description="ID of the building"),
    meter_type: str = Query(..., description="Type of meter (e.g. solar, electric)"),
    horizon: int = Query(3, ge=1, le=24, description="Hours to forecast ahead"),
    db: Session = Depends(get_db)
):
    """Generate a simple forecast based on recent readings."""
    readings = (
        db.query(SensorData)
        .filter_by(building_id=building_id, meter_type=meter_type)
        .order_by(SensorData.timestamp)
        .all()
    )

    if not readings:
        raise HTTPException(status_code=404, detail="No data found for given building/meter type")

    # Convert to DataFrame
    df = pd.DataFrame([{"timestamp": r.timestamp, "value": r.value} for r in readings])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Simple moving average forecast
    avg_value = df["value"].tail(3).mean()
    last_time = df["timestamp"].max()

    future_times = [last_time + pd.Timedelta(hours=i) for i in range(1, horizon + 1)]
    forecast_list = [
        {"timestamp": str(future_times[i]), "predicted_value": float(avg_value)} for i in range(horizon)
    ]

    return {
        "building_id": building_id,
        "meter_type": meter_type,
        "horizon_hours": horizon,
        "forecast": forecast_list
    }
