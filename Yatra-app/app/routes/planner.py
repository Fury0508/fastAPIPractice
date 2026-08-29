from fastapi import APIRouter, HTTPException
from models import TravelRequestModel
from service.weather import fetch_weather
from service.places import fetch_places
from service.currency import fetch_currency
import asyncio

router = APIRouter(
    prefix= "/plan",
    tags= [ 'planner'],
)

@router.post("/")
async def create_travel_plan(travel_request: TravelRequestModel):
    """ Aggregate Weather, Currency and Places data into a single travel plan."""
    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
    trip_days = (travel_request.end_date - travel_request.start_date).days
    if trip_days < 1:
        raise HTTPException(status_code=400, detail="Trip duration must be at least 1 day.")
    if trip_days > 14:
        raise HTTPException(status_code=400, detail="Trip duration cannot exceed 14 days.")

    #weather data

    # currency data
    # places data
    weather_data, places_data, currency_data = await asyncio.gather(
        fetch_weather(
            destination= travel_request.destination,
            start_date= travel_request.start_date,
            end_date=travel_request.end_date
        ),
        fetch_places(travel_request.destination),
        fetch_currency(travel_request.base_currency)
    )
    return {
        "message" : "Travel plan created Successfully",
        "destination" : travel_request.destination,
        "trip_days" : trip_days,
        "weather_data" : weather_data,
        "places_data" : places_data,
        "currency_data" : currency_data
    }