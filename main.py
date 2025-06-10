#!/usr/bin/env python3
"""
Smart Travel Assistant - Main Entry Point
Interactive command-line interface for flight status and analytics queries.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent
from agents.inquiry_router import InquiryRouterAgent


def main():
    """Main function to run the Smart Travel Assistant."""
    print("🛫 Smart Travel Assistant")
    print("=" * 50)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API keys from environment
    aviationstack_key = os.getenv('AVIATIONSTACK_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not aviationstack_key:
        print("Error: AVIATIONSTACK_API_KEY not found in .env file")
        return
    
    # Initialize Gemini client function if API key is available
    llm_client = None
    use_llm = False
    
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            def llm_client(prompt):
                response = model.generate_content(prompt)
                return response.text
            
            use_llm = True
            print("✅ Gemini LLM client initialized")
        except Exception as e:
            print(f"Warning: Could not initialize Gemini client: {e}")
            print("Falling back to regex-only routing")
    else:
        print("No GEMINI_API_KEY found, using regex-only routing")
    
    # Initialize agents
    print("Initializing agents...")
    try:
        status_agent = FlightStatusAgent(aviationstack_key)
        
        # Try to initialize analytics agent, but continue without it if BigQuery fails
        try:
            analytics_agent = FlightAnalyticsAgent()
            analytics_available = True
        except Exception as bq_error:
            print(f"⚠️  Warning: BigQuery not available ({bq_error})")
            print("Analytics features will be disabled. Status queries will still work.")
            analytics_agent = None
            analytics_available = False
        
        router = InquiryRouterAgent(status_agent, analytics_agent, use_llm=use_llm, llm_client=llm_client)
        routing_method = "LLM + regex fallback" if use_llm else "regex only"
        analytics_status = "enabled" if analytics_available else "disabled"
        print(f"✅ Agents initialized ({routing_method}, analytics {analytics_status})")
    except Exception as e:
        print(f"Error initializing agents: {e}")
        return
    
    # Interactive loop
    print("\nYou can ask about:")
    print("• Flight status (e.g., 'What's the status of AA123?')")
    print("• Cheapest fares (e.g., 'Cheapest fares from JNB to ELS in 2021')")
    print("• Type 'exit' to quit\n")
    
    while True:
        try:
            # Get user input
            user_query = input("Query: ").strip()
            
            # Check for exit condition
            if user_query.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            # Skip empty queries
            if not user_query:
                continue
            
            # Route query and get response
            response = router.handle_query(user_query)
            print(f"\n{response}\n")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error processing query: {e}")


if __name__ == "__main__":
    main() 