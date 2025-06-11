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
            analytics_agent: Agent instance with analyze_flight_data(query: str) -> str method for delay analytics
            use_llm (bool): Whether to use LLM for query classification. Defaults to False.
            llm_client: LLM client function that takes a prompt and returns a response
        """
        self.status_agent = status_agent
        self.analytics_agent = analytics_agent
        self.use_llm = use_llm
        self.llm_client = llm_client
        
        # Initialize conversational memory for routing context
        self.last_agent_used: str | None = None  # 'status' or 'analytics'
        self.last_query_type: str | None = None  # Track what type of query was last processed
        
        # Set up logging for routing decisions
        logging.basicConfig(level=logging.WARNING)
        self.logger = logging.getLogger(__name__)
        
        # Regex pattern to detect flight numbers (2-3 uppercase letters + 2-4 digits)
        self.flight_number_pattern = re.compile(r'\b[A-Z]{2,3}\d{2,4}\b')
        
        # LLM classification system prompt - updated for delay vs status with context awareness
        self.llm_system_prompt = '''You are a flight query classifier. Reply exactly "status" or "delay".

STATUS queries: Ask about specific flight numbers (e.g., "AA123", "DL456"). Examples:
- "What's the status of AA123?"
- "Is flight UA456 on time?"

DELAY queries: Ask about airlines, routes, delays, on-time performance, or day-of-week analysis between airports. Examples:
- "What are the most on-time airlines from SFO to JFK?"
- "Which day has fewer delays from EWR to ORD?" 
- "Show me airlines with best performance"

Follow-up phrases like "what about" should usually maintain the same type as previous queries.'''
        
        if self.use_llm and not self.llm_client:
            self.logger.warning("LLM routing enabled but no llm_client provided, falling back to regex")
            self.use_llm = False
        
        routing_method = "LLM + regex fallback" if self.use_llm else "regex only"
    
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
            return "💭 I'd love to help! Could you tell me what you'd like to know about flights? Try asking about a flight status or airline performance."
        
        query_clean = query.strip()
        
        # Check for follow-up phrases that should use conversational memory
        follow_up_phrases = ['what about', 'how about', 'and for', 'what if']
        is_follow_up = any(phrase in query_clean.lower() for phrase in follow_up_phrases)
        
        if is_follow_up and self.last_agent_used:
            if self.last_agent_used == "analytics":
                result = self._route_to_analytics(query_clean)
                self.last_agent_used = "analytics"
                return result
            elif self.last_agent_used == "status":
                result = self._route_to_status(query_clean)
                self.last_agent_used = "status"
                return result
        
        # Try LLM classification first if enabled
        if self.use_llm:
            llm_decision = self._classify_with_llm(query_clean)
            if llm_decision == "status":
                result = self._route_to_status(query_clean)
                self.last_agent_used = "status"
                return result
            elif llm_decision == "delay":
                result = self._route_to_analytics(query_clean)
                self.last_agent_used = "analytics"
                return result
            # If LLM fails or returns unknown, fall back to regex
            pass
        
        # Search for flight number pattern in the query (regex fallback or primary method)
        flight_number_match = self.flight_number_pattern.search(query_clean.upper())
        
        if flight_number_match:
            # Flight number detected - route to status agent
            flight_number = flight_number_match.group()
            
            try:
                result = self.status_agent.get_status(flight_number)
                self.last_agent_used = "status"
                return result
            except Exception as e:
                self.logger.error(f"Error calling status agent: {str(e)}")
                return f"😞 I ran into an issue checking that flight: {str(e)}"
        
        else:
            # No flight number detected - check for delay analysis keywords
            delay_keywords = [
                'delay', 'delays', 'on-time', 'on time', 'performance', 'airlines', 
                'best', 'worst', 'day of week', 'weekday', 'monday', 'tuesday', 
                'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'analytics',
                'analysis', 'compare', 'comparison', 'ranking', 'rank'
            ]
            
            has_delay_keywords = any(keyword in query_clean.lower() for keyword in delay_keywords)
            has_airport_codes = bool(re.search(r'\b[A-Z]{3}\b', query_clean.upper()))
            
            if has_delay_keywords or has_airport_codes:
                # Route to analytics agent
                
                # Check if analytics agent is available
                if not self.analytics_agent:
                    return "📊 Delay analytics are taking a quick break (BigQuery is resting). How about checking a specific flight status instead?"
                
                try:
                    result = self.analytics_agent.analyze_flight_data(query_clean)
                    self.last_agent_used = "analytics"
                    return result
                except Exception as e:
                    self.logger.error(f"Error calling analytics agent: {str(e)}")
                    return f"😅 I encountered a hiccup getting that delay information: {str(e)}"
            
            else:
                # Could not determine query type
                self.logger.warning("Could not determine query type")
                return ("I can help with two types of queries:\n"
                       "1. Flight status: Include a flight number (e.g., 'What's the status of AA123?')\n"
                       "2. Delay analysis: Ask about on-time performance, delays, or best days to fly (e.g., 'What are the most on-time airlines from SFO to JFK?')")
    
    def _classify_with_llm(self, query: str) -> str | None:
        """
        Use LLM to classify the query intent.
        
        Args:
            query (str): User query string
            
        Returns:
            str | None: "status", "delay", or None if classification fails
        """
        try:
            # Construct prompt with system message and user query
            prompt = f"{self.llm_system_prompt}\n\nUser query: {query}"
            
            response = self.llm_client(prompt)
            
            # Parse LLM response
            if isinstance(response, str):
                response_clean = response.strip().lower()
                if response_clean == "status":
                    return "status"
                elif response_clean == "delay":
                    return "delay"
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
            
            try:
                result = self.status_agent.get_status(flight_number)
                return result
            except Exception as e:
                self.logger.error(f"Error calling status agent: {str(e)}")
                return f"😞 I ran into an issue checking that flight: {str(e)}"
        else:
            self.logger.warning("LLM classified as status but no flight number found")
            return "✈️ I'd love to help with that flight! Please include a flight number like 'What's the status of AA123?'"
    
    def _route_to_analytics(self, query: str) -> str:
        """Route query to analytics agent for delay analysis."""
        # Check if analytics agent is available
        if not self.analytics_agent:
            return "📊 Delay analytics are taking a quick break (BigQuery is resting). How about checking a specific flight status instead?"
        
        try:
            result = self.analytics_agent.analyze_flight_data(query)
            return result
        except Exception as e:
            self.logger.error(f"Error calling analytics agent: {str(e)}")
            return f"📈 I hit a small bump analyzing that data: {str(e)}" 