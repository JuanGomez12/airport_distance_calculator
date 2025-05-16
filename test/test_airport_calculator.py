import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.append(str(Path(".").resolve()))  # Adjust the path to import AirportCalculator

from src.AirportCalculator import AirportCalculator


@pytest.fixture
def airport_calculator():
    return AirportCalculator()


@patch("src.AirportCalculator.airportsdata.load")
def test_get_airport_info_valid(mock_load, airport_calculator):
    mock_load.return_value = {
        "LAX": {"lat": 33.9425, "lon": -118.4081},
        "JFK": {"lat": 40.6413, "lon": -73.7781},
    }
    airport_calculator.airports = mock_load.return_value
    airport_info = airport_calculator.get_airport_info("LAX")
    assert airport_info["lat"] == 33.9425
    assert airport_info["lon"] == -118.4081


@patch("src.AirportCalculator.airportsdata.load")
def test_get_airport_info_invalid(mock_load, airport_calculator):
    mock_load.return_value = {"LAX": {"lat": 33.9425, "lon": -118.4081}}
    airport_calculator.airports = mock_load.return_value
    with pytest.raises(ValueError):
        airport_calculator.get_airport_info("INVALID")


@patch("src.AirportCalculator.airportsdata.load")
@patch("src.AirportCalculator.DistanceCalculator.vincenty")
def test_calculate_distance_vincenty(mock_vincenty, mock_load, airport_calculator):
    mock_load.return_value = {
        "LAX": {"lat": 33.9425, "lon": -118.4081},
        "JFK": {"lat": 40.6413, "lon": -73.7781},
    }
    airport_calculator.airports = mock_load.return_value
    mock_vincenty.return_value = 3974.336  # Mocked distance in km
    distance = airport_calculator.calculate_distance("LAX", "JFK")
    assert distance == 3974.336


@patch("src.AirportCalculator.airportsdata.load")
@patch("src.AirportCalculator.DistanceCalculator.vincenty")
@patch("src.AirportCalculator.DistanceCalculator.haversine")
def test_calculate_distance_fallback_to_haversine(mock_haversine, mock_vincenty, mock_load, airport_calculator):
    mock_load.return_value = {
        "LAX": {"lat": 33.9425, "lon": -118.4081},
        "JFK": {"lat": 40.6413, "lon": -73.7781},
    }
    airport_calculator.airports = mock_load.return_value
    mock_vincenty.side_effect = Exception("Vincenty calculation failed")
    mock_haversine.return_value = 3983.0  # Mocked fallback distance in km
    distance = airport_calculator.calculate_distance("LAX", "JFK")
    assert distance == 3983.0


@patch("src.AirportCalculator.airportsdata.load")
@patch("src.AirportCalculator.DistanceCalculator.vincenty")
def test_calculate_multipart_distance(mock_vincenty, mock_load, airport_calculator):
    mock_load.return_value = {
        "LAX": {"lat": 33.9425, "lon": -118.4081},
        "JFK": {"lat": 40.6413, "lon": -73.7781},
        "ORD": {"lat": 41.9742, "lon": -87.9073},
    }
    airport_calculator.airports = mock_load.return_value
    mock_vincenty.side_effect = [3974.336, 1180.0]  # Mocked distances in km
    total_distance = airport_calculator.calculate_multipart_distance(["LAX", "JFK", "ORD"])
    assert total_distance == pytest.approx(5154.336, 0.1)
