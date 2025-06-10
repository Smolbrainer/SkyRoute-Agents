from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest, Forbidden
import logging


class FlightAnalyticsAgent:
    """Agent responsible for performing analytics queries on flight data using Google BigQuery."""
    
    def __init__(self):
        """
        Initialize the FlightAnalyticsAgent with BigQuery client using Application Default Credentials.
        
        Raises:
            Exception: If BigQuery client initialization fails
        """
        try:
            # Initialize BigQuery client with Application Default Credentials
            # Using project from gcloud configuration: clear-heaven-462504-r3
            self.client = bigquery.Client(project="clear-heaven-462504-r3")
            # Set up logging for debugging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            raise Exception(f"Failed to initialize BigQuery client: {str(e)}")
    
    def get_cheapest_fares(self, origin: str, destination: str, year: int, limit: int = 5) -> str:
        """
        Retrieve the cheapest flight fares between two airports for a given year.
        Uses aviation airlines data from flight aggregators with global coverage.
        
        Args:
            origin (str): Origin airport code (e.g., "LAX", "JFK")
            destination (str): Destination airport code (e.g., "SFO", "ORD") 
            year (int): Year to analyze (e.g., 2023, 2024)
            limit (int, optional): Maximum number of results to return. Defaults to 5.
            
        Returns:
            str: Human-readable summary of cheapest flight fares
        """
        try:
            # Validate input parameters
            if not origin or not destination:
                return "Error: Both origin and destination airport codes are required."
            
            if year < 1990 or year > 2030:
                return "Error: Please provide a valid year between 1990 and 2030."
                
            if limit < 1 or limit > 50:
                return "Error: Limit must be between 1 and 50 results."
            
            # Parameterized SQL query to find cheapest fares
            query = """
            SELECT
                dataprovider,
                flight_number,
                departure_date,
                departure_airport,
                arrival_airport,
                price
            FROM
                `clear-heaven-462504-r3.aviation_airlines_data_from_flight_aggregators_global_coverage.Aviation Datasets`
            WHERE
                (departure_airport = @origin OR departure_airport LIKE CONCAT('%(', @origin, ')'))
                AND (arrival_airport = @destination OR arrival_airport LIKE CONCAT('%(', @destination, ')'))
                AND EXTRACT(YEAR FROM PARSE_DATETIME('%m/%d/%Y %H:%M', departure_date)) = @year
                AND price IS NOT NULL
                AND price > 0
            ORDER BY 
                price ASC
            LIMIT @limit
            """
            
            # Configure query parameters to prevent SQL injection
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("origin", "STRING", origin.upper()),
                    bigquery.ScalarQueryParameter("destination", "STRING", destination.upper()),
                    bigquery.ScalarQueryParameter("year", "INT64", year),
                    bigquery.ScalarQueryParameter("limit", "INT64", limit),
                ]
            )
            
            # Execute the query
            self.logger.info(f"Executing query for {origin} to {destination} in {year}")
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()  # Wait for query completion
            
            # Convert results to list for processing
            flights = list(results)
            
            # Handle case when no data is found
            if not flights:
                return f"No flight fare data found for routes from {origin.upper()} to {destination.upper()} in {year}. This could be due to limited data availability in the public dataset."
            
            # Format results into human-readable summary
            summary = f"Cheapest flight fares from {origin.upper()} to {destination.upper()} in {year}:\n\n"
            
            for i, flight in enumerate(flights, 1):
                # Extract flight details with safe defaults
                provider = flight.dataprovider or "Unknown Provider"
                flight_num = flight.flight_number or "Unknown"
                dep_airport = flight.departure_airport or origin.upper()
                arr_airport = flight.arrival_airport or destination.upper()
                departure_date = flight.departure_date or "Unknown Date"
                price = flight.price if flight.price is not None else 0
                
                # Format individual flight entry
                summary += f"{i}. Flight {flight_num}\n"
                summary += f"   Route: {dep_airport} → {arr_airport}\n" 
                summary += f"   Date: {departure_date}\n"
                summary += f"   Price: ${price:,.2f}\n"
                summary += f"   Provider: {provider}\n\n"
            
            # Add helpful context information
            if len(flights) == limit:
                summary += f"Note: Showing top {limit} cheapest fares. There may be additional options available."
            else:
                summary += f"Total of {len(flights)} flight options found."
                
            return summary.strip()
            
        except NotFound:
            return "Error: The BigQuery dataset or table was not found. Please verify access permissions."
            
        except Forbidden:
            return "Error: Access denied to BigQuery. Please ensure you have proper authentication and permissions."
            
        except BadRequest as e:
            return f"Error: Invalid query parameters or syntax. Details: {str(e)}"
            
        except Exception as e:
            self.logger.error(f"Unexpected error in get_cheapest_fares: {str(e)}")
            return f"An unexpected error occurred while analyzing flight fares: {str(e)}" 