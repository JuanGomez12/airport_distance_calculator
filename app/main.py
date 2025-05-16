from pathlib import Path
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, StringConstraints

from src.AirportCalculator import AirportCalculator
from src.utils.logger import get_logger

logger = get_logger(Path(__file__).stem)

app = FastAPI()


class airport(BaseModel):
    iata_code: Annotated[str, StringConstraints(min_length=3, max_length=3)]


class airports(BaseModel):
    iata_codes: list[airport]


airport_calculator = AirportCalculator()


@app.post("/calculate_distance/")
async def calculate_distance(airports: airports):
    iata_codes = [airport.iata_code for airport in airports.iata_codes]
    logger.info("Calculating distance for airports: %s", iata_codes)
    return {"distance_km": airport_calculator.calculate_multipart_distance(iata_codes)}


@app.get("/health")
def check_health() -> dict:
    """Performs a health check on the server, to see if it's alive.

    Returns:
        dict: Dictionary containing the status.
    """
    return {"status": "ok"}
