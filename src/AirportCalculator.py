import logging
from math import atan2, cos, radians, sin, sqrt

import airportsdata
from vincenty import vincenty

logger = logging.getLogger(__name__)
logger_format = "[%(asctime)s - %(filename)s:%(lineno)s] - %(funcName)s() - %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=logger_format)


class DistanceCalculator:
    @staticmethod
    def haversine(point1: tuple, point2: tuple) -> float:
        """
        Calculate the great-circle distance between two points on the Earth specified in decimal degrees.
        """
        # Convert decimal degrees to radians
        lat1, lon1 = map(radians, point1)
        lat2, lon2 = map(radians, point2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        r = 6371.0
        return c * r  # returns distance in kilometers

    @staticmethod
    def vincenty(point1: tuple, point2: tuple) -> float:
        """
        Calculate the distance between two points on the Earth using the Vincenty formula.
        """
        return vincenty(point1, point2)


class AirportCalculator:
    def __init__(self):
        self.airports = airportsdata.load("IATA")

    def get_airport_info(self, iata_code: str) -> dict:
        """
        Retrieves information about an airport based on its IATA code.
        Args:
            iata_code (str): The 3-letter IATA code of the airport.
        Returns:
            dict: A dictionary containing information about the airport.
        Raises:
            ValueError: If the IATA code is invalid (not 3 characters long or not found in the airport database).
        """

        if len(iata_code) > 3 or iata_code not in self.airports:
            raise ValueError(f"Invalid IATA code: {iata_code}")
        return self.airports[iata_code]

    def calculate_distance(self, iata_start: str, iata_end: str) -> float:
        """
        Calculate the distance between two airports using their IATA codes.

        Args:
            iata_start (str): The IATA code of the starting airport.
            iata_end (str): The IATA code of the destination airport.

        Returns:
            float: The distance between the two airports in kilometers.
        """
        airport_start = self.get_airport_info(iata_start)
        airport_end = self.get_airport_info(iata_end)

        point1 = airport_start["lat"], airport_start["lon"]
        point2 = airport_end["lat"], airport_end["lon"]

        try:
            distance = DistanceCalculator.vincenty(point1, point2)
        except Exception as e:
            error_message = f"Error calculating distance between {iata_start} and {iata_end} using vincenty: {e}, falling back to haversine"
            logger.error(error_message)
            distance = DistanceCalculator.haversine(point1, point2)
        return distance

    def calculate_multipart_distance(self, iata_codes: list) -> float:
        """
        Calculate the total distance for a series of airports, in the order they are provided.
        This method calculates the distance between each consecutive pair of airports in the list.
        The distance is calculated using the IATA codes of the airports.

        Args:
            iata_codes (list): A list of IATA codes.

        Returns:
            float: The total distance in kilometers.
        """
        total_distance = 0.0
        for i in range(len(iata_codes) - 1):
            total_distance += self.calculate_distance(iata_codes[i], iata_codes[i + 1])
        return total_distance


if __name__ == "__main__":
    from pprint import pprint

    airport_calculator = AirportCalculator()
    pprint(airport_calculator.get_airport_info("LAX"))
    print(airport_calculator.calculate_distance("LAX", "JFK"), "km")
    print(airport_calculator.calculate_multipart_distance(["LAX", "JFK", "ORD"]), "km")
