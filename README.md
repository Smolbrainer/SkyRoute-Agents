# SkyRoute Agents - Smart Travel Assistant ✈️

A sophisticated conversational AI system that provides intelligent flight analytics with memory, real-time flight status, and user-friendly natural language interactions using AviationStack API and Google BigQuery.

## 🌟 Project Overview

SkyRoute Agents is a next-generation multi-agent system that revolutionizes how users interact with flight data. The system employs conversational AI with memory to provide personalized, context-aware travel assistance through natural language interactions.

### 🤖 Core Agents

- **InquiryRouterAgent**: 🧠 **AI-powered central orchestrator** with conversational memory that intelligently routes queries using advanced pattern matching and optional Gemini LLM integration
- **FlightStatusAgent**: 📡 **Enhanced real-time tracker** with robust error handling for flight information, delays, gate changes, and supports 2-3 letter airline codes
- **FlightAnalyticsAgent**: 📊 **Conversational analytics engine** leveraging Google BigQuery for intelligent performance analysis with contextual memory and complex multi-dimensional analytics

## 🚀 What's New & Enhanced

### 🧠 **Conversational Memory System**
Revolutionary context retention that makes interactions natural and efficient:
- **Memory Persistence**: Remembers query types, airports, dates, and user preferences
- **Intelligent Follow-ups**: "What about from SFO to DEN?" automatically applies previous analysis type
- **Context Switching**: Seamlessly transitions between different types of analyses
- **Smart Parameter Inheritance**: Reuses relevant information from previous queries

### 🎯 **AI-Powered User Experience**
Complete interface overhaul focused on user delight:
- **Friendly Welcome**: "✈️ Welcome to SkyRoute Agents - Your Smart Travel Assistant! ✈️"
- **Encouraging Prompts**: "🗣️ Ask me anything:" instead of cold command prompts
- **Helpful Error Messages**: "✈️ I need both airports to help you! Try 'SFO to JFK'" 
- **Clean Output**: Removed technical logging for professional user experience
- **Emoji Enhancement**: Visual cues that make the interface approachable and fun

### 🔍 **Enhanced Flight Recognition**
Improved pattern matching for broader airline support:
- **Extended Airline Codes**: Now supports 2-3 letter codes (AA123, ACA1185, WN2077)
- **Smart Filtering**: Automatically excludes common non-airport 3-letter words
- **Robust Parsing**: Better handling of various query formats and patterns
- **Context-Aware Extraction**: Intelligent airport code detection in natural language

### 🛡️ **Bulletproof Error Handling**
Comprehensive resilience for production-ready reliability:
- **Null-Safe Operations**: Prevents "NoneType" errors from API responses
- **Graceful Degradation**: System continues working even when components fail
- **User-Friendly Messages**: Technical errors translated to helpful guidance
- **Recovery Suggestions**: Actionable advice when things go wrong

### 📊 **Advanced Analytics Engine**
Sophisticated analysis capabilities beyond basic queries:
- **Multi-Dimensional Metrics**: Departure delays, arrival delays, on-time percentages
- **Day-of-Week Intelligence**: "Which day has the least delays from LAX to ORD?"
- **Performance Rankings**: Airlines sorted by actual performance metrics
- **Statistical Significance**: Only includes airlines with sufficient data
- **Smart Recommendations**: AI-powered suggestions with clear explanations

## 🎯 Core Features

### Real-Time Flight Status
- **Live Updates**: Current flight information with departure/arrival times
- **Delay Notifications**: Real-time delay and gate change information
- **Comprehensive Details**: Airline information, aircraft type, route details
- **Robust API Integration**: Reliable data from AviationStack with error recovery

### 🆕 **Conversational Flight Analytics**
- **On-Time Performance Rankings**: Airlines ranked by delay performance with detailed metrics
- **Day-of-Week Analysis**: Discover the best days to fly with comprehensive delay breakdowns
- **Natural Follow-Ups**: Continue conversations seamlessly across multiple queries
- **Contextual Memory**: System remembers your preferences and previous questions
- **Historical Insights**: Performance trends and patterns over time
- **Smart Filtering**: Only meaningful results with statistical significance

### 🧠 **Intelligent Query Processing**
- **Natural Language Understanding**: Ask questions however feels comfortable
- **Intent Detection**: Automatically determines what type of analysis you want
- **Parameter Extraction**: Smart parsing of airports, dates, and preferences
- **Context Preservation**: Maintains conversation flow across multiple interactions
- **Flexible Formats**: Supports various ways of asking the same question

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- AviationStack API key (free tier available at [aviationstack.com](https://aviationstack.com))
- Google Cloud account with BigQuery access
- Optional: Gemini API key for enhanced AI routing

### Quick Start
1. **Clone and Setup Environment**:
   ```bash
   git clone [repository-url]
   cd SkyRoute-Agents-1
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

4. **Set Up API Keys**:
   Create a `.env` file in the project root:
   ```env
   AVIATIONSTACK_API_KEY=your_aviationstack_key_here
   GEMINI_API_KEY=your_gemini_key_here  # Optional for enhanced routing
   ```

5. **Launch the Assistant**:
   ```bash
   python main.py
   ```

## 💬 Interactive Examples

### Flight Status with Enhanced Recognition
```
🗣️  Ask me anything: Whats the status of AC1185

🤔 Let me check that for you...

Flight AC1185 (Air Canada) - Status: Scheduled
From: Lester B. Pearson International (Scheduled: 2025-06-12T20:30)
To: Port Columbus International (Scheduled: 2025-06-12T21:51)
```

### 🆕 **Conversational Analytics Flow**
```
🗣️  Ask me anything: What are the most on-time airlines from JFK to ATL?

🤔 Let me check that for you...

Airlines ranked by on-time performance from JFK to ATL:

#1. Endeavor Air Inc. (9E)
    Average overall delay: 1.4 minutes
    Average departure delay: 1.4 minutes
    Average arrival delay: 1.3 minutes
    On-time performance: 83.6% (≤15 min delay)
    Total flights analyzed: 55

#2. Delta Air Lines Inc. (DL)
    Average overall delay: 8.5 minutes
    Average departure delay: 10.6 minutes
    Average arrival delay: 6.3 minutes
    On-time performance: 79.2% (≤15 min delay)
    Total flights analyzed: 1,874

Note: On-time performance is defined as flights arriving within 15 minutes of scheduled time.
Airlines with fewer than 10 flights on this route are excluded from rankings.

-------------------------------------------------------
🗣️  Ask me anything: What about JFK to ORD?

🤔 Let me check that for you...

Airlines ranked by on-time performance from JFK to ORD:

#1. American Airlines Inc. (AA)
    Average overall delay: 16.2 minutes
    Average departure delay: 24.1 minutes
    Average arrival delay: 8.3 minutes
    On-time performance: 74.0% (≤15 min delay)
    Total flights analyzed: 365

#2. JetBlue Airways (B6)
    Average overall delay: 16.3 minutes
    Average departure delay: 18.0 minutes
    Average arrival delay: 14.7 minutes
    On-time performance: 69.6% (≤15 min delay)
    Total flights analyzed: 905

#3. Endeavor Air Inc. (9E)
    Average overall delay: 17.2 minutes
    Average departure delay: 22.0 minutes
    Average arrival delay: 12.3 minutes
    On-time performance: 71.3% (≤15 min delay)
    Total flights analyzed: 1,056

Note: On-time performance is defined as flights arriving within 15 minutes of scheduled time.
Airlines with fewer than 10 flights on this route are excluded from rankings.

-------------------------------------------------------
🗣️  Ask me anything: Which day has the fewest delays?

🤔 Let me check that for you...

Flight delays by day of week from JFK to ORD:

#1. Saturday
    Average overall delay: 11.8 minutes
    Average departure delay: 17.7 minutes
    Average arrival delay: 6.0 minutes
    On-time performance: 76.4%
    Total flights: 330

#2. Tuesday
    Average overall delay: 11.9 minutes
    Average departure delay: 15.6 minutes
    Average arrival delay: 8.2 minutes
    On-time performance: 71.6%
    Total flights: 335

#3. Sunday
    Average overall delay: 16.2 minutes
    Average departure delay: 19.9 minutes
    Average arrival delay: 12.6 minutes
    On-time performance: 70.5%
    Total flights: 329

#4. Wednesday
    Average overall delay: 16.9 minutes
    Average departure delay: 20.8 minutes
    Average arrival delay: 13.0 minutes
    On-time performance: 75.3%
    Total flights: 332

#5. Monday
    Average overall delay: 18.5 minutes
    Average departure delay: 22.2 minutes
    Average arrival delay: 14.9 minutes
    On-time performance: 68.9%
    Total flights: 334

#6. Friday
    Average overall delay: 19.6 minutes
    Average departure delay: 22.7 minutes
    Average arrival delay: 16.5 minutes
    On-time performance: 65.8%
    Total flights: 333

#7. Thursday
    Average overall delay: 21.8 minutes
    Average departure delay: 26.6 minutes
    Average arrival delay: 17.1 minutes
    On-time performance: 69.1%
    Total flights: 333

✅ **Saturday** has the least delays with an average of 11.8 minutes overall delay.
```

## 🏗️ Advanced Architecture

### 🧠 **Conversational AI System**
- **Memory-Enabled Agents**: Each agent maintains contextual information across interactions
- **Intent Preservation**: System remembers what type of analysis you prefer
- **Smart Routing**: AI-powered decision making with graceful regex fallbacks
- **Natural Language Processing**: Advanced query parsing and parameter extraction

### 🛡️ **Production-Ready Design**
- **Fault Tolerance**: System continues working even when individual components fail
- **Graceful Degradation**: Features disable cleanly when dependencies are unavailable
- **Comprehensive Error Handling**: User-friendly messages for all error conditions
- **Security Best Practices**: Environment variables, parameterized queries, input validation

### 📊 **Analytics Infrastructure**
- **BigQuery Integration**: Scalable analytics on large flight datasets
- **Optimized Queries**: Performance-tuned SQL for complex multi-dimensional analysis
- **Statistical Validation**: Results filtered for significance and reliability
- **Real-Time Processing**: Live data analysis with sub-second response times

### 🎨 **User Experience Design**
- **Conversational Interface**: Natural language interactions with memory
- **Visual Enhancement**: Emoji-rich interface that's both professional and approachable
- **Progressive Disclosure**: Information presented at the right level of detail
- **Error Recovery**: Helpful guidance when queries need clarification

## 🤖 Developer API

### FlightAnalyticsAgent - Conversational Interface
```python
from agents.flight_analytics_agent import FlightAnalyticsAgent

# Initialize with conversational memory
agent = FlightAnalyticsAgent()

# Natural language queries with automatic context retention
result1 = agent.analyze_flight_data("What are the most on-time airlines from SFO to JFK?")
print(result1)

# Follow-up queries automatically use context
result2 = agent.analyze_flight_data("What about from LAX to ORD?")  # Remembers analysis type
result3 = agent.analyze_flight_data("Which day has fewer delays?")  # Remembers route

# Direct method access for programmatic use
airlines = agent.get_on_time_airlines("DEN", "ATL", year=2023, limit=5)
days = agent.get_day_of_week_delays("SFO", "JFK", year=2023)
```

### InquiryRouterAgent - Smart Routing
```python
from agents.inquiry_router import InquiryRouterAgent
from agents.flight_status_agent import FlightStatusAgent
from agents.flight_analytics_agent import FlightAnalyticsAgent

# Initialize with optional AI enhancement
status_agent = FlightStatusAgent(api_key)
analytics_agent = FlightAnalyticsAgent()
router = InquiryRouterAgent(status_agent, analytics_agent, use_llm=True, llm_client=gemini_client)

# Intelligent routing with memory
response1 = router.handle_query("What's the status of WN2077?")  # Routes to status
response2 = router.handle_query("What are the best airlines from SFO to JFK?")  # Routes to analytics  
response3 = router.handle_query("What about from LAX to DEN?")  # Uses memory
```

## 📊 Analytics Capabilities

### 🎯 **Performance Analysis**
- **Multi-Metric Rankings**: Departure delays, arrival delays, overall performance
- **On-Time Calculations**: Industry-standard 15-minute threshold analysis
- **Volume Statistics**: Flight counts for statistical significance
- **Comparative Analysis**: Head-to-head airline performance comparisons

### 📅 **Temporal Analysis**
- **Day-of-Week Patterns**: Discover optimal travel days
- **Seasonal Trends**: Performance variations over time
- **Historical Analysis**: Year-over-year comparisons
- **Peak Time Analysis**: Performance during high-traffic periods

### 🧠 **Conversational Intelligence**
- **Context Retention**: Remembers preferences across sessions
- **Smart Follow-ups**: Natural conversation flow
- **Intent Detection**: Understands what you're looking for
- **Parameter Inheritance**: Reuses relevant information automatically

## 🔒 Security & Reliability

- **Environment Variable Security**: API keys safely stored and managed
- **SQL Injection Prevention**: Parameterized queries throughout
- **Input Validation**: Comprehensive sanitization and validation
- **Error Isolation**: Failures contained to prevent system-wide issues
- **Graceful Degradation**: Core features continue working during partial outages

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Repository**: Create your own copy
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Add your improvements
4. **Test Thoroughly**: Ensure everything works
5. **Submit Pull Request**: Share your contribution

### Development Guidelines
- Follow existing code style and patterns
- Add tests for new features
- Update documentation for changes
- Ensure backward compatibility

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎯 Mission**: Make flight data accessible through natural conversation  
**🧠 Intelligence**: Conversational AI + Memory + Smart Analytics  
**🛡️ Reliability**: Production-ready error handling + graceful degradation  
**🎨 Experience**: User-friendly interface with delightful interactions  
**🔮 Future**: Expanding AI capabilities for even smarter travel assistance 
