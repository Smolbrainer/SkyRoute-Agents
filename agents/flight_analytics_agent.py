from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest, Forbidden
import logging
from typing import Optional, Dict, Any
import re


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
            # Set up logging for debugging - only show warnings and errors
            logging.basicConfig(level=logging.WARNING)
            self.logger = logging.getLogger(__name__)
            
            # Initialize conversational memory
            self.memory: Dict[str, Any] = {
                'last_query_type': None,
                'last_origin': None,
                'last_destination': None,
                'last_year': None,
                'last_limit': None
            }
        except Exception as e:
            raise Exception(f"Failed to initialize BigQuery client: {str(e)}")
    
    def analyze_flight_data(self, query: str) -> str:
        """
        Main entry point for flight data analysis. Routes queries to appropriate methods
        and handles conversational memory.
        
        Args:
            query (str): Natural language query about flight data
            
        Returns:
            str: Analysis results
        """
        try:
            # Parse the query to extract intent and parameters
            parsed_query = self._parse_query(query)
            
            if 'error' in parsed_query:
                return parsed_query['error']
            
            # Route to appropriate analysis method
            if parsed_query['type'] == 'day_of_week_delays':
                result = self.get_day_of_week_delays(
                    origin=parsed_query['origin'],
                    destination=parsed_query['destination'],
                    year=parsed_query.get('year')
                )
            elif parsed_query['type'] == 'on_time_airlines':
                result = self.get_on_time_airlines(
                    origin=parsed_query['origin'],
                    destination=parsed_query['destination'],
                    year=parsed_query.get('year'),
                    limit=parsed_query.get('limit', 10)
                )
            else:
                # Default to on-time airlines analysis
                result = self.get_on_time_airlines(
                    origin=parsed_query['origin'],
                    destination=parsed_query['destination'],
                    year=parsed_query.get('year'),
                    limit=parsed_query.get('limit', 10)
                )
            
            # Update memory with this query
            self._update_memory(parsed_query)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in analyze_flight_data: {str(e)}")
            return f"😅 I encountered an error while analyzing your query: {str(e)}"
    
    def _parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query to extract intent and parameters.
        Uses conversational memory for context.
        """
        query_lower = query.lower()
        parsed: Dict[str, Any] = {}
        
        # Determine query type
        if any(phrase in query_lower for phrase in ['day of week', 'which day', 'what day', 'weekday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']):
            parsed['type'] = 'day_of_week_delays'
        else:
            parsed['type'] = 'on_time_airlines'
        
        # Extract airport codes - look for 3-letter codes that are likely airports
        # Common patterns: "from SFO to JFK", "SFO to JFK", "SFO-JFK", etc.
        airport_pattern = r'\b([A-Z]{3})\b'
        potential_codes = re.findall(airport_pattern, query.upper())
        
        # Filter out common non-airport 3-letter words
        common_words = {'THE', 'AND', 'FOR', 'ARE', 'YOU', 'TOP', 'DAY', 'HAS', 'FEW', 'WHO', 'WHY', 'HOW', 'CAN', 'GET', 'SET', 'RUN', 'NEW', 'OLD', 'BIG', 'BAD', 'END', 'USE', 'WAY', 'MAN', 'SEE', 'HIM', 'TWO', 'NOW', 'ITS', 'DID', 'YES', 'HIS', 'HER', 'SHE', 'HAS', 'HAD', 'HIS', 'HER', 'HIM', 'WHO', 'OIL', 'SIT', 'SET', 'BUT', 'NOT', 'ALL', 'ANY', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'TRY', 'WAY', 'WIN', 'OWN', 'SAY', 'TOO', 'USE', 'TWO', 'NEW', 'NOW', 'OLD', 'SEE', 'HIM', 'ITS', 'LET', 'PUT', 'END', 'WHY', 'TRY', 'ASK', 'RUN', 'OWN', 'SIT', 'SET', 'GET', 'GOT', 'HAS', 'HIT', 'HOT', 'JOB', 'LET', 'LOT', 'MAP', 'MEN', 'NET', 'PET', 'RUN', 'SUN', 'TEN', 'VAN', 'WIN', 'YES', 'YET', 'ZOO'}
        airport_codes = [code for code in potential_codes if code not in common_words]
        
        if len(airport_codes) >= 2:
            parsed['origin'] = airport_codes[0]
            parsed['destination'] = airport_codes[1]
        elif len(airport_codes) == 1:
            # Use conversational memory to fill in missing airport
            if 'what about' in query_lower or 'how about' in query_lower:
                if self.memory['last_origin'] and self.memory['last_destination']:
                    # User is asking about a different route, try to determine which airport changed
                    if airport_codes[0] != self.memory['last_origin'] and airport_codes[0] != self.memory['last_destination']:
                        # New airport, keep the previous query type
                        parsed['type'] = self.memory['last_query_type'] or parsed['type']
                        parsed['origin'] = airport_codes[0]
                        parsed['destination'] = self.memory['last_destination']
                    else:
                        parsed['origin'] = self.memory['last_origin']
                        parsed['destination'] = airport_codes[0]
            else:
                # Need both airports
                return {'error': '✈️ I need both airports to help you! Try something like "SFO to JFK" or "from LAX to ORD"'}
        elif len(airport_codes) == 0:
            # No airports found, check if this is a follow-up question or if we should use memory
            follow_up_phrases = ['what about', 'how about', 'and for', 'which day', 'what day', 'fewer delays']
            if (any(phrase in query_lower for phrase in follow_up_phrases) and 
                self.memory['last_origin'] and self.memory['last_destination']):
                # Use memory for airports
                parsed['origin'] = self.memory['last_origin']
                parsed['destination'] = self.memory['last_destination']
                # For questions without specific airports but asking about analysis, use memory context
                if 'what about' in query_lower or 'how about' in query_lower:
                    # For "what about" questions, preserve the analysis type unless explicitly changed
                    if parsed['type'] == 'on_time_airlines' and self.memory['last_query_type']:
                        parsed['type'] = self.memory['last_query_type']
            else:
                return {'error': '✈️ I need to know which airports you\'re interested in! Try "SFO to JFK" or "from Miami to Seattle"'}
        else:
            return {'error': '✈️ I need both airports to help you! Try something like "SFO to JFK" or "from LAX to ORD"'}
        
        # Extract year if mentioned
        year_match = re.search(r'\b(19|20)\d{2}\b', query)
        if year_match:
            parsed['year'] = int(year_match.group())
        elif self.memory['last_year'] and ('what about' in query_lower or 'how about' in query_lower):
            parsed['year'] = self.memory['last_year']
        
        # Extract limit if mentioned
        limit_match = re.search(r'\btop\s+(\d+)\b|\b(\d+)\s+airlines\b', query_lower)
        if limit_match:
            parsed['limit'] = int(limit_match.group(1) or limit_match.group(2))
        elif self.memory['last_limit'] and ('what about' in query_lower or 'how about' in query_lower):
            parsed['limit'] = self.memory['last_limit']
        
        return parsed
    
    def _update_memory(self, parsed_query: Dict[str, Any]):
        """Update conversational memory with the latest query."""
        self.memory['last_query_type'] = parsed_query['type']
        self.memory['last_origin'] = parsed_query.get('origin')
        self.memory['last_destination'] = parsed_query.get('destination')
        self.memory['last_year'] = parsed_query.get('year')
        self.memory['last_limit'] = parsed_query.get('limit')
    
    def get_on_time_airlines(self, origin: str, destination: str, year: Optional[int] = None, limit: int = 10) -> str:
        """
        Analyze on-time performance of airlines for flights between two airports.
        Returns airlines ranked by their average delay performance.
        
        Args:
            origin (str): Origin airport code (e.g., "SFO", "JFK")
            destination (str): Destination airport code (e.g., "JFK", "LAX") 
            year (int, optional): Year to analyze. If None, analyzes all available years.
            limit (int, optional): Maximum number of airlines to return. Defaults to 10.
            
        Returns:
            str: Human-readable summary of airlines ranked by on-time performance
        """
        try:
            # Validate input parameters
            if not origin or not destination:
                return "🏃‍♂️ I need both departure and arrival airports to find the best airlines for you!"
            
            if year is not None and (year < 1990 or year > 2030):
                return "📅 That year seems a bit unusual! Could you try a year between 1990 and 2030?"
                
            if limit < 1 or limit > 50:
                return "📊 I can show you between 1 and 50 airlines. How about picking a number in that range?"
            
            # Build base query for on-time performance analysis
            base_query = """
            SELECT
                carrier,
                name as airline_name,
                COUNT(*) as total_flights,
                AVG(COALESCE(dep_delay, 0)) as avg_dep_delay,
                AVG(COALESCE(arr_delay, 0)) as avg_arr_delay,
                AVG((COALESCE(dep_delay, 0) + COALESCE(arr_delay, 0)) / 2) as avg_overall_delay,
                SUM(CASE WHEN COALESCE(arr_delay, 0) <= 15 THEN 1 ELSE 0 END) / COUNT(*) * 100 as on_time_percentage
            FROM
                `clear-heaven-462504-r3.flights.flights`
            WHERE
                origin = @origin
                AND dest = @destination
                AND carrier IS NOT NULL
                AND name IS NOT NULL
            """
            
            # Add year filter if specified
            query_parameters = [
                bigquery.ScalarQueryParameter("origin", "STRING", origin.upper()),
                bigquery.ScalarQueryParameter("destination", "STRING", destination.upper()),
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
            ]
            
            if year is not None:
                base_query += " AND year = @year"
                query_parameters.append(bigquery.ScalarQueryParameter("year", "INT64", year))
            
            # Complete the query with grouping and ordering
            query = base_query + """
            GROUP BY
                carrier, name
            HAVING
                COUNT(*) >= 10  -- Only include airlines with sufficient data
            ORDER BY 
                avg_overall_delay ASC, on_time_percentage DESC
            LIMIT @limit
            """
            
            # Configure query parameters to prevent SQL injection
            job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
            
            # Execute the query
            year_str = f" in {year}" if year else ""
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()  # Wait for query completion
            
            # Convert results to list for processing
            airlines = list(results)
            
            # Handle case when no data is found
            if not airlines:
                year_clause = f" in {year}" if year else ""
                return f"🔍 I couldn't find any flights on that route{year_clause}. This might be because it's not a common route or the data is limited. Try a major city pair like SFO to JFK!"
            
            # Format results into human-readable summary
            year_text = f" in {year}" if year else ""
            summary = f"Airlines ranked by on-time performance from {origin.upper()} to {destination.upper()}{year_text}:\n\n"
            
            for i, airline in enumerate(airlines, 1):
                # Extract airline details with safe defaults
                carrier_code = airline.carrier or "Unknown"
                airline_name = airline.airline_name or f"Carrier {carrier_code}"
                total_flights = airline.total_flights or 0
                avg_dep_delay = airline.avg_dep_delay or 0
                avg_arr_delay = airline.avg_arr_delay or 0
                avg_overall_delay = airline.avg_overall_delay or 0
                on_time_percentage = airline.on_time_percentage or 0
                
                # Format individual airline entry
                summary += f"#{i}. {airline_name} ({carrier_code})\n"
                summary += f"    Average overall delay: {avg_overall_delay:.1f} minutes\n"
                summary += f"    Average departure delay: {avg_dep_delay:.1f} minutes\n" 
                summary += f"    Average arrival delay: {avg_arr_delay:.1f} minutes\n"
                summary += f"    On-time performance: {on_time_percentage:.1f}% (≤15 min delay)\n"
                summary += f"    Total flights analyzed: {total_flights:,}\n\n"
            
            # Add helpful context information
            summary += "Note: On-time performance is defined as flights arriving within 15 minutes of scheduled time.\n"
            summary += "Airlines with fewer than 10 flights on this route are excluded from rankings."
                
            return summary.strip()
            
        except NotFound:
            return "🔧 I'm having trouble accessing the flight database. This is usually temporary - please try again in a moment!"
            
        except Forbidden:
            return "🔐 I don't have permission to access the flight data right now. This should be fixed soon!"
            
        except BadRequest as e:
            return f"🤔 Something about that request didn't work quite right. Could you try rephrasing? (Technical details: {str(e)})"
            
        except Exception as e:
            self.logger.error(f"Unexpected error in get_on_time_airlines: {str(e)}")
            return f"😅 Something unexpected happened while looking up airline performance. Please try again! (Details: {str(e)})"
    
    def get_day_of_week_delays(self, origin: str, destination: str, year: Optional[int] = None) -> str:
        """
        Analyze flight delays by day of the week for a specific route.
        
        Args:
            origin (str): Origin airport code (e.g., "SFO", "JFK")
            destination (str): Destination airport code (e.g., "JFK", "LAX") 
            year (Optional[int]): Year to analyze. If None, analyzes all available years.
            
        Returns:
            str: Human-readable summary of delays by day of week
        """
        try:
            # Validate input parameters
            if not origin or not destination:
                return "🏃‍♂️ I need both departure and arrival airports to analyze delays by day!"
            
            if year is not None and (year < 1990 or year > 2030):
                return "📅 That year seems outside my range! Could you try a year between 1990 and 2030?"
            
            # Build query for day-of-week analysis
            base_query = """
            SELECT
                EXTRACT(DAYOFWEEK FROM DATE(year, month, day)) as day_of_week,
                COUNT(*) as total_flights,
                AVG(COALESCE(dep_delay, 0)) as avg_dep_delay,
                AVG(COALESCE(arr_delay, 0)) as avg_arr_delay,
                AVG((COALESCE(dep_delay, 0) + COALESCE(arr_delay, 0)) / 2) as avg_overall_delay,
                SUM(CASE WHEN COALESCE(arr_delay, 0) <= 15 THEN 1 ELSE 0 END) / COUNT(*) * 100 as on_time_percentage
            FROM
                `clear-heaven-462504-r3.flights.flights`
            WHERE
                origin = @origin
                AND dest = @destination
                AND year IS NOT NULL
                AND month IS NOT NULL
                AND day IS NOT NULL
            """
            
            # Add year filter if specified
            query_parameters = [
                bigquery.ScalarQueryParameter("origin", "STRING", origin.upper()),
                bigquery.ScalarQueryParameter("destination", "STRING", destination.upper()),
            ]
            
            if year is not None:
                base_query += " AND year = @year"
                query_parameters.append(bigquery.ScalarQueryParameter("year", "INT64", year))
            
            # Complete the query with grouping and ordering
            query = base_query + """
            GROUP BY
                day_of_week
            HAVING
                COUNT(*) >= 5  -- Only include days with sufficient data
            ORDER BY 
                avg_overall_delay ASC
            """
            
            # Configure query parameters
            job_config = bigquery.QueryJobConfig(query_parameters=query_parameters)
            
            # Execute the query
            year_str = f" in {year}" if year else ""
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()
            
            # Convert results to list for processing
            day_data = list(results)
            
            # Handle case when no data is found
            if not day_data:
                year_clause = f" in {year}" if year else ""
                return f"🔍 I couldn't find any flights on that route{year_clause}. Try a popular route like JFK to ORD!"
            
            # Map day numbers to day names (BigQuery DAYOFWEEK: 1=Sunday, 2=Monday, etc.)
            day_names = {
                1: "Sunday", 2: "Monday", 3: "Tuesday", 4: "Wednesday",
                5: "Thursday", 6: "Friday", 7: "Saturday"
            }
            
            # Format results
            year_text = f" in {year}" if year else ""
            summary = f"Flight delays by day of week from {origin.upper()} to {destination.upper()}{year_text}:\n\n"
            
            for i, day in enumerate(day_data, 1):
                day_name = day_names.get(day.day_of_week, f"Day {day.day_of_week}")
                total_flights = day.total_flights or 0
                avg_dep_delay = day.avg_dep_delay or 0
                avg_arr_delay = day.avg_arr_delay or 0
                avg_overall_delay = day.avg_overall_delay or 0
                on_time_percentage = day.on_time_percentage or 0
                
                # Format individual day entry
                summary += f"#{i}. {day_name}\n"
                summary += f"    Average overall delay: {avg_overall_delay:.1f} minutes\n"
                summary += f"    Average departure delay: {avg_dep_delay:.1f} minutes\n"
                summary += f"    Average arrival delay: {avg_arr_delay:.1f} minutes\n"
                summary += f"    On-time performance: {on_time_percentage:.1f}%\n"
                summary += f"    Total flights: {total_flights:,}\n\n"
            
            # Find the best day
            if day_data:
                best_day = min(day_data, key=lambda x: x.avg_overall_delay or float('inf'))
                best_day_name = day_names.get(best_day.day_of_week, f"Day {best_day.day_of_week}")
                summary += f"✅ **{best_day_name}** has the least delays with an average of {best_day.avg_overall_delay:.1f} minutes overall delay."
            
            return summary.strip()
            
        except NotFound:
            return "🔧 I'm having trouble accessing the flight database. Please try again in a moment!"
            
        except Forbidden:
            return "🔐 I don't have permission to access the flight data right now. Should be back up soon!"
            
        except BadRequest as e:
            return f"🤔 Something about that request needs tweaking. Could you rephrase it? (Technical: {str(e)})"
            
        except Exception as e:
            self.logger.error(f"Unexpected error in get_day_of_week_delays: {str(e)}")
            return f"😅 I hit an unexpected snag analyzing those delays. Please try again! (Details: {str(e)})"
    
    def test_routing(self) -> str:
        """
        Test method to validate query routing and conversational memory.
        Returns a summary of how different queries would be routed.
        """
        test_queries = [
            "What are the most on-time airlines from SFO to JFK?",
            "Which day of the week has the least delays from LAX to ORD?",
            "Show me top 5 airlines for SFO to DEN",
            "What about from SFO to BOS?",  # Memory test
            "Which day has fewer delays?",   # Memory test
        ]
        
        results = []
        results.append("=== Flight Analytics Agent Routing Test ===\n")
        
        for i, query in enumerate(test_queries, 1):
            try:
                parsed = self._parse_query(query)
                results.append(f"{i}. Query: '{query}'")
                results.append(f"   Parsed: {parsed}")
                results.append(f"   Route: {parsed.get('type', 'unknown')}")
                results.append("")
            except Exception as e:
                results.append(f"{i}. Query: '{query}' - ERROR: {str(e)}")
                results.append("")
        
        results.append(f"Memory state: {self.memory}")
        return "\n".join(results) 