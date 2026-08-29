from pydantic import BaseModel
from datetime import date
from typing import Optional
class TravelRequestModel(BaseModel):
    destination: str
    start_date: date
    end_date: date
    base_currency: str = "USD"

class WeatherResponseModel(BaseModel):
    date: str
    condition: str
    temperature_high: float
    temperature_low: float
    humidity: float
    rain_chance: float


class PlacesResponseModel(BaseModel):
    name: str
    description: str
    category: str
    rating: float
    esttimated_time_hours: str
    entry_fee: Optional[float] = None