#!/usr/bin/env python3
"""
SkyRoute Agents - Smart Travel Assistant
Interactive command-line interface for flight status and delay analytics queries.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent
from agents.inquiry_router import InquiryRouterAgent


def main():
    """Main function to run the SkyRoute Agents Smart Travel Assistant."""
    print("✈️  Welcome to SkyRoute Agents - Your Smart Travel Assistant! ✈️")
    print("=" * 65)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API keys from environment
    aviationstack_key = os.getenv('AVIATIONSTACK_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    if not aviationstack_key:
        print("❌ Oops! I couldn't find your AVIATIONSTACK_API_KEY in the .env file.")
        print("💡 Please add your API key to continue using flight status features.")
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
            print("🤖 Great! I've connected to Gemini AI for smarter query understanding")
        except Exception as e:
            print(f"⚠️  Heads up: I couldn't connect to Gemini AI ({e})")
            print("🔄 Don't worry! I'll use my built-in understanding instead")
    else:
        print("💡 No Gemini AI key found - I'll use my built-in query understanding")
    
    # Initialize agents
    print("🚀 Setting up your travel assistant...")
    try:
        status_agent = FlightStatusAgent(aviationstack_key)
        
        # Try to initialize analytics agent, but continue without it if BigQuery fails
        try:
            analytics_agent = FlightAnalyticsAgent()
            analytics_available = True
        except Exception as bq_error:
            print(f"⚠️  Flight delay analytics temporarily unavailable: {bq_error}")
            print("✅ Flight status tracking is ready! Delay analytics will be added back soon.")
            analytics_agent = None
            analytics_available = False
        
        router = InquiryRouterAgent(status_agent, analytics_agent, use_llm=use_llm, llm_client=llm_client)
        ai_mode = "🤖 AI-powered" if use_llm else "🔍 Pattern-based"
        analytics_status = "enabled" if analytics_available else "coming soon"
        print(f"✅ Ready to help! ({ai_mode} understanding, delay analytics {analytics_status})")
    except Exception as e:
        print(f"😞 Sorry, I ran into a setup issue: {e}")
        print("💡 Please check your configuration and try again")
        return
    
    # Interactive loop  
    print("\n🎯 I'm here to help with your flight needs! Try asking me about:")
    print("   🔍 Flight tracking → 'What's the status of AA123?'")
    if analytics_available:
        print("   📊 Airline performance → 'Which airlines are most on-time from EWR to SFO?'")
        print("   📅 Best travel days → 'Which day has the least delays from JFK to ATL?'")
        print("   💬 Follow-up questions → 'What about from LGA to ORD?'")
    print("   ❌ Exit anytime → Just type 'exit'\n")
    
    print("💡 Tip: I understand natural language, so feel free to ask however feels comfortable!\n")
    
    while True:
        try:
            # Get user input
            user_query = input("🗣️  Ask me anything: ").strip()
            
            # Check for exit condition
            if user_query.lower() == 'exit':
                print("\n👋 Thanks for using SkyRoute Agents! Have a great trip! ✈️")
                break
            
            # Skip empty queries
            if not user_query:
                print("💭 I'm here when you're ready to ask something!")
                continue
            
            # Route query and get response
            print("\n🤔 Let me check that for you...")
            response = router.handle_query(user_query)
            print(f"\n{response}\n")
            print("-" * 55)
            
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using SkyRoute Agents! Safe travels! ✈️")
            break
        except Exception as e:
            print(f"😅 Oops, something unexpected happened: {e}")
            print("💡 Please try rephrasing your question or check your connection")


if __name__ == "__main__":
    main() 