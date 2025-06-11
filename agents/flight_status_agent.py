import requests
from typing import Optional


class FlightStatusAgent:
    """Agent responsible for fetching real-time flight status information from AviationStack API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the FlightStatusAgent with AviationStack API credentials.
        
        Args:
            api_key (str): AviationStack API access key
        """
        self.api_key = api_key
        self.base_url = "http://api.aviationstack.com/v1/flights"
    
    def get_status(self, flight_number: str) -> str:
        """
        Retrieve current status information for a specific flight.
        
        Args:
            flight_number (str): Flight number (e.g., "AA123", "DL456")
            
        Returns:
            str: Human-readable flight status information
        """
        try:
            # Prepare API request parametersGEMINI_API_KEY
            params = {
                'access_key': self.api_key,
                'flight_iata': flight_number.upper()  # Ensure uppercase for consistency
            }
            
            # Make request to AviationStack API with timeout
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            data = response.json()
            
            # Check if API returned any flight data
            if not data.get('data') or len(data['data']) == 0:
                return f"🔍 I couldn't find flight {flight_number}. Could you double-check the flight number? Airlines sometimes change flight numbers!"
            
            # Extract first flight result (most recent)
            flight_data = data['data'][0]
            
            # Parse key flight information with robust null checks
            airline_info = flight_data.get('airline') or {}
            airline = airline_info.get('name', 'Unknown airline')
            flight_status = flight_data.get('flight_status', 'Unknown status')
            
            # Extract departure information safely
            departure = flight_data.get('departure') or {}
            dep_airport = departure.get('airport', 'Unknown')
            dep_scheduled = departure.get('scheduled', 'N/A')
            dep_actual = departure.get('actual', 'N/A')
            
            # Extract arrival information safely
            arrival = flight_data.get('arrival') or {}
            arr_airport = arrival.get('airport', 'Unknown')
            arr_scheduled = arrival.get('scheduled', 'N/A')
            arr_estimated = arrival.get('estimated', 'N/A')
            
            # Format human-readable response
            status_msg = f"Flight {flight_number} ({airline}) - Status: {flight_status.title()}\n"
            status_msg += f"From: {dep_airport} (Scheduled: {dep_scheduled[:16] if dep_scheduled and dep_scheduled != 'N/A' else 'N/A'})\n"
            status_msg += f"To: {arr_airport} (Scheduled: {arr_scheduled[:16] if arr_scheduled and arr_scheduled != 'N/A' else 'N/A'})"
            
            # Add delay information if available
            if dep_actual and dep_actual != 'N/A' and dep_actual != dep_scheduled:
                status_msg += f"\nActual Departure: {dep_actual[:16]}"
            if arr_estimated and arr_estimated != 'N/A' and arr_estimated != arr_scheduled:
                status_msg += f"\nEstimated Arrival: {arr_estimated[:16]}"
                
            return status_msg
            
        except requests.exceptions.Timeout:
            return f"⏰ The flight data service is taking a bit longer than usual for {flight_number}. Please give it another try!"
            
        except requests.exceptions.ConnectionError:
            return f"🌐 I'm having trouble connecting to get flight info. Could you check your internet connection and try again?"
            
        except requests.exceptions.HTTPError as e:
            return f"📡 I ran into an issue with the flight data service (error {e.response.status_code}). This usually resolves quickly!"
            
        except Exception as e:
            return f"Unexpected error while fetching flight status: {str(e)}" 