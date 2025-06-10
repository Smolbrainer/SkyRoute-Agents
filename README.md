# Smart Travel Assistant

A multi-agent Python system that provides intelligent flight status and fare analytics using AviationStack API and Google BigQuery.

## Project Overview

The Smart Travel Assistant employs a modular multi-agent architecture with three specialized agents:

- **InquiryRouterAgent**: Central orchestration layer that routes queries using regex patterns or optional LLM classification
- **FlightStatusAgent**: Integrates with AviationStack API for real-time flight information, delays, and gate changes
- **FlightAnalyticsAgent**: Leverages Google BigQuery to analyze historical flight data and pricing trends

An optional LLM enhancement using Gemini Flash provides sophisticated natural language understanding for query classification, with graceful fallback to regex-based routing.

## Features

### Flight Status Queries
- Real-time flight status information
- Departure and arrival times
- Gate information
- Delay notifications
- Airline details

### Fare Analytics
- Historical fare analysis
- Cheapest routes between airports
- Price trends by year
- Multiple airline comparisons
- Flexible date range queries

### Airport Code Handling
The system supports multiple airport code formats:
- IATA codes (e.g., "JNB")
- Full airport names with IATA codes (e.g., "O.R Tambo Int. Airport (JNB)")
- Automatic format detection and conversion

## Setup & Run

### Prerequisites
- Python 3.8+
- AviationStack API key (free tier available)
- Google Cloud account with BigQuery access
- Optional: Gemini API key for enhanced routing

### Installation
1. Clone the repository and navigate to the project directory
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up Google Cloud authentication:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
5. Create a `.env` file with your API keys:
   ```
   AVIATIONSTACK_API_KEY=your_aviationstack_key_here
   GEMINI_API_KEY=your_gemini_key_here
   ```
6. Add `.env` to your `.gitignore` file (already included in the repository)

### Run the Application
```bash
python main.py
```

## Query Examples

### Flight Status Query
```
Query: What's the status of AA123?

Flight AA123 (American Airlines) - Status: Landed
From: Dallas/Fort Worth International (Scheduled: 2025-06-09T11:11)
To: Kahului (Scheduled: 2025-06-09T14:00)
Actual Departure: 2025-06-09T11:37
```

### Fare Analytics Query
```
Query: Cheapest flight fares from JNB to ELS in 2021

Cheapest flight fares from JNB to ELS in 2021:

1. Flight FA 388
   Route: O.R Tambo Int. Airport (JNB) → East London Airport (ELS)
   Date: 12/15/2021 7:10
   Price: $2,000.00
   Provider: FlySafair

2. Flight FA 382
   Route: O.R Tambo Int. Airport (JNB) → East London Airport (ELS)
   Date: 12/15/2021 15:40
   Price: $2,290.00
   Provider: FlySafair

3. Flight FA 240
   Route: O.R Tambo Int. Airport (JNB) → East London Airport (ELS)
   Date: 12/15/2021 11:35
   Price: $2,369.00
   Provider: FlySafair

4. Flight FA 382
   Route: O.R Tambo Int. Airport (JNB) → East London Airport (ELS)
   Date: 12/17/2021 15:40
   Price: $2,421.00
   Provider: FlySafair

5. Flight FA 240
   Route: O.R Tambo Int. Airport (JNB) → East London Airport (ELS)
   Date: 12/17/2021 11:35
   Price: $3,271.00
   Provider: FlySafair

Note: Showing top 5 cheapest fares. There may be additional options available.
```

## Design Choices

### Modular Architecture
- Each agent operates independently with well-defined APIs
- Enables horizontal scaling and fault isolation
- Easy to add new features or modify existing ones

### Intelligent Routing
- Primary routing using flight number regex patterns (`\b[A-Z]{2}\d{2,4}\b`)
- Optional LLM enhancement for complex queries
- Graceful fallback to regex when LLM is unavailable

### Database Integration
- Secure parameterized queries to prevent SQL injection
- Flexible airport code handling (IATA codes and full names)
- Proper datetime parsing for accurate date-based queries
- Comprehensive error handling for database operations

### Security Features
- Environment variables for sensitive data
- Parameterized SQL queries
- Input validation and sanitization
- Proper error handling and logging
- Secure credential management

### Error Handling
- Comprehensive exception handling
- User-friendly error messages
- Graceful degradation of features
- Detailed logging for debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Architecture**: Multi-agent system with AviationStack + BigQuery integration  
**Routing**: Regex + optional LLM (Gemini Flash) classification  
**Security**: Environment variables, parameterized queries, graceful error handling  
**Database**: Flexible airport code handling, secure queries, proper datetime parsing 