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
🗣️ Ask me anything: What's the status of ACA1185?

🤔 Let me check that for you...

Flight ACA1185 (Air Canada) - Status: Active
From: Toronto Pearson International (Scheduled: 2025-01-15T14:30)
To: Vancouver International (Scheduled: 2025-01-15T17:45)
Actual Departure: 2025-01-15T14:42
Estimated Arrival: 2025-01-15T17:38
```

### 🆕 **Conversational Analytics Flow**
```
🗣️ Ask me anything: What are the most on-time airlines from SFO to JFK?

🤔 Let me check that for you...

Airlines ranked by on-time performance from SFO to JFK:

#1. Delta Air Lines (DL)
    Average overall delay: 2.3 minutes
    Average departure delay: 3.1 minutes
    Average arrival delay: 1.5 minutes
    On-time performance: 79.2% (≤15 min delay)
    Total flights analyzed: 1,247

#2. United Airlines (UA)
    Average overall delay: 4.8 minutes
    Average departure delay: 6.2 minutes
    Average arrival delay: 3.4 minutes
    On-time performance: 73.8% (≤15 min delay)
    Total flights analyzed: 892

#3. JetBlue Airways (B6)
    Average overall delay: 7.1 minutes
    Average departure delay: 8.9 minutes
    Average arrival delay: 5.3 minutes
    On-time performance: 69.4% (≤15 min delay)
    Total flights analyzed: 634

Note: On-time performance is defined as flights arriving within 15 minutes of scheduled time.
Airlines with fewer than 10 flights on this route are excluded from rankings.

-------------------------------------------------------
🗣️ Ask me anything: What about from LAX to ORD?

🤔 Let me check that for you...

Airlines ranked by on-time performance from LAX to ORD:
[System automatically applies on-time airline analysis to the new route]

-------------------------------------------------------
🗣️ Ask me anything: Which day has fewer delays?

🤔 Let me check that for you...

Flight delays by day of week from LAX to ORD:
[System remembers the LAX to ORD route and analyzes day-of-week patterns]
```

### 🆕 **Day-of-Week Intelligence**
```
🗣️ Ask me anything: Which day of the week has the least delays from SFO to DEN?

🤔 Let me check that for you...

Flight delays by day of week from SFO to DEN:

#1. Tuesday
    Average overall delay: 5.2 minutes
    Average departure delay: 6.8 minutes
    Average arrival delay: 3.6 minutes
    On-time performance: 76.3%
    Total flights: 892

#2. Wednesday  
    Average overall delay: 7.1 minutes
    Average departure delay: 8.9 minutes
    Average arrival delay: 5.3 minutes
    On-time performance: 72.1%
    Total flights: 834

#3. Saturday
    Average overall delay: 8.4 minutes
    Average departure delay: 10.2 minutes
    Average arrival delay: 6.6 minutes
    On-time performance: 69.7%
    Total flights: 756

✅ **Tuesday** has the least delays with an average of 5.2 minutes overall delay.
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