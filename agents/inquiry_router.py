import re
import logging
from typing import Any


class InquiryRouterAgent:
    """Agent responsible for routing user queries to appropriate specialized agents based on query content."""
    
    def __init__(self, status_agent: Any, analytics_agent: Any, use_llm: bool = False, llm_client: Any = None):
        """
        Initialize the InquiryRouterAgent with worker agents.
        
        Args:
            status_agent: Agent instance with get_status(flight_number: str) -> str method
            analytics_agent: Agent instance with get_cheapest_fares(origin: str, destination: str, year: int, limit: int) -> str method
            use_llm (bool): Whether to use LLM for query classification. Defaults to False.
            llm_client: LLM client function that takes a prompt and returns a response
        """
        self.status_agent = status_agent
        self.analytics_agent = analytics_agent
        self.use_llm = use_llm
        self.llm_client = llm_client
        
        # Set up logging for routing decisions
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Regex pattern to detect flight numbers (2 uppercase letters + 2-4 digits)
        self.flight_number_pattern = re.compile(r'\b[A-Z]{2}\d{2,4}\b')
        
        # LLM classification system prompt
        self.llm_system_prompt = 'You are a classifier. Reply exactly "status" or "price".'
        
        if self.use_llm and not self.llm_client:
            self.logger.warning("LLM routing enabled but no llm_client provided, falling back to regex")
            self.use_llm = False
        
        routing_method = "LLM + regex fallback" if self.use_llm else "regex only"
        self.logger.info(f"InquiryRouterAgent initialized with {routing_method} routing")
    
    def handle_query(self, query: str) -> str:
        """
        Route user query to appropriate agent based on content analysis.
        
        Args:
            query (str): User's travel-related query
            
        Returns:
            str: Response from the appropriate agent or error message
        """
        if not query or not query.strip():
            self.logger.warning("Empty query received")
            return "Please provide a valid query. I can help with flight status (e.g., 'AA123') or fare analysis."
        
        query_clean = query.strip()
        self.logger.info(f"Processing query: '{query_clean[:50]}{'...' if len(query_clean) > 50 else ''}'")
        
        # Try LLM classification first if enabled
        if self.use_llm:
            llm_decision = self._classify_with_llm(query_clean)
            if llm_decision == "status":
                return self._route_to_status(query_clean)
            elif llm_decision == "price":
                return self._route_to_analytics(query_clean)
            # If LLM fails or returns unknown, fall back to regex
            self.logger.info("LLM classification failed or returned unknown response, falling back to regex")
        
        # Search for flight number pattern in the query (regex fallback or primary method)
        flight_number_match = self.flight_number_pattern.search(query_clean.upper())
        
        if flight_number_match:
            # Flight number detected - route to status agent
            flight_number = flight_number_match.group()
            self.logger.info(f"Flight number '{flight_number}' detected, routing to status agent")
            
            try:
                result = self.status_agent.get_status(flight_number)
                self.logger.info("Successfully retrieved flight status information")
                return result
            except Exception as e:
                self.logger.error(f"Error calling status agent: {str(e)}")
                return f"Error retrieving flight status: {str(e)}"
        
        else:
            # No flight number detected - attempt to route to analytics agent
            self.logger.info("No flight number detected, attempting to route to analytics agent")
            
            # Check if analytics agent is available
            if not self.analytics_agent:
                return ("Analytics features are currently unavailable (BigQuery not configured).\n"
                       "I can help with flight status queries. Include a flight number (e.g., 'What's the status of AA123?')")
            
            # Try to parse origin, destination, and year from query
            parsed_params = self._parse_analytics_query(query_clean)
            
            if parsed_params:
                origin, destination, year, limit = parsed_params
                self.logger.info(f"Parsed analytics parameters: {origin} -> {destination}, year {year}, limit {limit}")
                
                try:
                    result = self.analytics_agent.get_cheapest_fares(origin, destination, year, limit)
                    self.logger.info("Successfully retrieved fare analytics information")
                    return result
                except Exception as e:
                    self.logger.error(f"Error calling analytics agent: {str(e)}")
                    return f"Error retrieving fare analytics: {str(e)}"
            
            else:
                # Could not parse required parameters
                self.logger.warning("Could not parse analytics query parameters")
                return ("I can help with two types of queries:\n"
                       "1. Flight status: Include a flight number (e.g., 'What's the status of AA123?')\n"
                       "2. Fare analysis: Specify route and year (e.g., 'Cheapest fares from LAX to JFK in 2023')")
    
    def _parse_analytics_query(self, query: str) -> tuple:
        """
        Attempt to parse origin, destination, year, and limit from analytics query.
        
        Args:
            query (str): User query string
            
        Returns:
            tuple: (origin, destination, year, limit) if successful, None if parsing fails
        """
        try:
            # Convert to uppercase for easier parsing
            query_upper = query.upper()
            
            # Look for airport codes (3-letter IATA codes are common, but also handle 2-letter)
            airport_pattern = re.compile(r'\b[A-Z]{3}\b')
            airports = airport_pattern.findall(query_upper)
            
            # Look for year (4-digit number between 1990-2030)
            year_pattern = re.compile(r'\b(19[9][0-9]|20[0-3][0-9])\b')
            year_match = year_pattern.search(query)
            
            # Look for limit/number keywords
            limit = 5  # default
            limit_pattern = re.compile(r'\b(?:top|limit|first|show)\s+(\d+)\b', re.IGNORECASE)
            limit_match = limit_pattern.search(query)
            if limit_match:
                limit = min(int(limit_match.group(1)), 50)  # Cap at 50
            
            # Validate we have minimum required parameters
            if len(airports) >= 2 and year_match:
                origin = airports[0]
                destination = airports[1]
                year = int(year_match.group(1))
                
                self.logger.info(f"Successfully parsed: {origin} -> {destination}, {year}, limit {limit}")
                return (origin, destination, year, limit)
            
            # Try alternative parsing for "from X to Y" pattern
            route_pattern = re.compile(r'\bfrom\s+([A-Z]{2,3})\s+to\s+([A-Z]{2,3})\b', re.IGNORECASE)
            route_match = route_pattern.search(query_upper)
            
            if route_match and year_match:
                origin = route_match.group(1).upper()
                destination = route_match.group(2).upper()
                year = int(year_match.group(1))
                
                self.logger.info(f"Successfully parsed route pattern: {origin} -> {destination}, {year}, limit {limit}")
                return (origin, destination, year, limit)
            
            self.logger.warning("Could not extract required parameters (origin, destination, year) from query")
            return None
            
        except Exception as e:
            self.logger.error(f"Error parsing analytics query: {str(e)}")
            return None
    
    def _classify_with_llm(self, query: str) -> str:
        """
        Use LLM to classify the query intent.
        
        Args:
            query (str): User query string
            
        Returns:
            str: "status", "price", or None if classification fails
        """
        try:
            # Construct prompt with system message and user query
            prompt = f"{self.llm_system_prompt}\n\nUser query: {query}"
            
            self.logger.info("Sending query to LLM for classification")
            response = self.llm_client(prompt)
            
            # Parse LLM response
            if isinstance(response, str):
                response_clean = response.strip().lower()
                if response_clean == "status":
                    self.logger.info("LLM classified query as: status")
                    return "status"
                elif response_clean == "price":
                    self.logger.info("LLM classified query as: price")
                    return "price"
                else:
                    self.logger.warning(f"LLM returned unexpected response: {response_clean}")
                    return None
            else:
                self.logger.warning(f"LLM returned non-string response: {type(response)}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error during LLM classification: {str(e)}")
            return None
    
    def _route_to_status(self, query: str) -> str:
        """Route query to status agent, extracting flight number if needed."""
        # Try to extract flight number from query
        flight_number_match = self.flight_number_pattern.search(query.upper())
        
        if flight_number_match:
            flight_number = flight_number_match.group()
            self.logger.info(f"Flight number '{flight_number}' detected, routing to status agent")
            
            try:
                result = self.status_agent.get_status(flight_number)
                self.logger.info("Successfully retrieved flight status information")
                return result
            except Exception as e:
                self.logger.error(f"Error calling status agent: {str(e)}")
                return f"Error retrieving flight status: {str(e)}"
        else:
            self.logger.warning("LLM classified as status but no flight number found")
            return "Please include a flight number for status queries (e.g., 'What's the status of AA123?')"
    
    def _route_to_analytics(self, query: str) -> str:
        """Route query to analytics agent, parsing parameters as needed."""
        # Check if analytics agent is available
        if not self.analytics_agent:
            return "Analytics features are currently unavailable (BigQuery not configured). Please try a flight status query instead."
        
        # Try to parse origin, destination, and year from query
        parsed_params = self._parse_analytics_query(query)
        
        if parsed_params:
            origin, destination, year, limit = parsed_params
            self.logger.info(f"Parsed analytics parameters: {origin} -> {destination}, year {year}, limit {limit}")
            
            try:
                result = self.analytics_agent.get_cheapest_fares(origin, destination, year, limit)
                self.logger.info("Successfully retrieved fare analytics information")
                return result
            except Exception as e:
                self.logger.error(f"Error calling analytics agent: {str(e)}")
                return f"Error retrieving fare analytics: {str(e)}"
        else:
            self.logger.warning("LLM classified as price but could not parse required parameters")
            return "For fare analysis, please specify route and year (e.g., 'Cheapest fares from LAX to JFK in 2023')" 