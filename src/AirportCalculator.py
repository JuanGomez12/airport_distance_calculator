import airportsdata


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

        if len(iata_end) > 3 or iata_end not in self.airports:
            raise ValueError(f"Invalid IATA code: {iata_end}")
        self.get_airport_info(iata_start)
        self.get_airport_info(iata_end)
        return 0.0

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
