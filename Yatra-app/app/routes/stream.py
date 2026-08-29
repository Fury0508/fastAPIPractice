from fastapi import APIRouter, HTTPException
from models import TravelRequestModel
from fastapi.responses import StreamingResponse
import json
from service.weather import fetch_weather
from service.places import fetch_places
from service.currency import fetch_currency
router = APIRouter(
    prefix= "/stream",
    tags= [ 'stream'],)


def format_sse(data: str, event: str = None) -> str:
    """Format a string as a Server-Sent Event (SSE)."""
    json_data = json.dumps(data)
    return f"data: {json_data}\n\n" if event is None else f"event: {event}\ndata: {json_data}\n\n"



async def stream_generator(travel_request: TravelRequestModel):
    """Generator function to stream travel plan data."""
    yield format_sse({"message": "Starting travel plan aggregation..."}, event="start")
    yield format_sse({"message": "Fetching weather data..."}, event="weather")
    weather_data = await fetch_weather(
        destination=travel_request.destination,
        start_date=travel_request.start_date,
        end_date=travel_request.end_date
    )
    # Handle both dict and Pydantic model responses
    weather_dict = weather_data if isinstance(weather_data, dict) else (
        [item.model_dump() if hasattr(item, 'model_dump') else item for item in weather_data] if isinstance(weather_data, list) else weather_data.model_dump()
    )
    yield format_sse({"weather_data": weather_dict}, event="weather_complete")
    
    yield format_sse({"message": "Fetching places data..."}, event="places")
    places_data = await fetch_places(travel_request.destination)
    # Handle both dict and Pydantic model responses
    places_dict = places_data if isinstance(places_data, dict) else (
        [item.model_dump() if hasattr(item, 'model_dump') else item for item in places_data] if isinstance(places_data, list) else places_data.model_dump()
    )
    yield format_sse({"places_data": places_dict}, event="places_complete")
    
    yield format_sse({"message": "Fetching currency data..."}, event="currency")
    currency_data = await fetch_currency(travel_request.base_currency)
    # Handle both dict and Pydantic model responses
    currency_dict = currency_data if isinstance(currency_data, dict) else (
        [item.model_dump() if hasattr(item, 'model_dump') else item for item in currency_data] if isinstance(currency_data, list) else currency_data.model_dump()
    )
    yield format_sse({"currency_data": currency_dict}, event="currency_complete")
    
    yield format_sse({"message": "Travel plan aggregation complete."}, event="complete")


@router.post("/plan", response_class=StreamingResponse)
async def stream_travel_plan(travel_request: TravelRequestModel):
    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(status_code=400, detail="Start date cannot be after end date.")
    trip_days = (travel_request.end_date - travel_request.start_date).days
    if trip_days < 1:
        raise HTTPException(status_code=400, detail="Trip duration must be at least 1 day.")
    if trip_days > 14:
        raise HTTPException(status_code=400, detail="Trip duration cannot exceed 14 days.")
    

    return StreamingResponse(
        stream_generator(travel_request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache","Connection": "keep-alive"},
    )