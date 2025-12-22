WEB SCRAPER - EDUCATIONAL PROJECT

IMPORTANT DISCLAIMER: This project uses BeautifulSoup and Selenium to scrape publicly available data from sources that permit scraping. This is for learning purposes only. Always check robots.txt and Terms of Service before scraping any website.

================================================================================
PROBLEM STATEMENT
================================================================================

The task is to build a web scraper that accepts a search term from a user, fetches relevant results from a public API or scrape-friendly source, and extracts contact information including names, emails, and phone numbers.

Example: User inputs "restaurants in coimbatore" → System fetches top 10 results → Extracts contact details → Returns formatted data to user.

================================================================================
PURPOSE
================================================================================

This project demonstrates:
- How to use Selenium for browser automation
- How to use BeautifulSoup for HTML parsing
- How to handle asynchronous content loading
- How to extract and structure data
- How to build a simple web interface
- How to process and return structured data

This is for educational understanding of web scraping mechanics only.

================================================================================
FILE STRUCTURE
================================================================================

project_root/
  |
  +-- backend/
  |     +-- requirements.txt
  |     +-- scraper.py
  |     +-- data_processor.py
  |     +-- app.py
  |
  +-- frontend/
  |     +-- index.html
  |     +-- style.css
  |     +-- script.js
  |
  +-- README.md

================================================================================
FILE DESCRIPTIONS & IMPORTANT METHODS
================================================================================

1. REQUIREMENTS.TXT
   Purpose: Lists all Python dependencies

   Contents:
   - selenium (version 4.0+) - Browser automation
   - beautifulsoup4 (version 4.9+) - HTML parsing
   - requests (version 2.25+) - HTTP requests
   - flask (version 2.0+) - Web framework
   - python-dotenv (version 0.19+) - Environment variables
   - lxml (version 4.6+) - XML/HTML processing

================================================================================

2. SCRAPER.PY
   Purpose: Core scraping logic using Selenium and BeautifulSoup

   Important Methods:

   a) initialize_driver()
      Parameters: None
      Returns: WebDriver object
      Functionality: Sets up Chrome WebDriver with options for headless browsing
      
   b) search_business_directory(search_term)
      Parameters: search_term (string) - What to search for
      Returns: List of URLs containing results
      Functionality: Uses a public business API to fetch result URLs
      Note: Uses Google Maps API or similar permitted services
      
   c) scrape_single_page(url)
      Parameters: url (string) - Website to scrape
      Returns: Dictionary with name, email, phone
      Functionality: Opens URL with Selenium, waits for content, parses HTML
      
   d) extract_contact_info(page_source)
      Parameters: page_source (string) - HTML content
      Returns: Dictionary with contact details
      Functionality: Uses regex and BeautifulSoup to find emails, phones, names
      
   e) scrape_all_results(urls_list)
      Parameters: urls_list (list) - List of URLs to scrape
      Returns: List of dictionaries with contact info
      Functionality: Loops through URLs, calls scrape_single_page for each

================================================================================

3. DATA_PROCESSOR.PY
   Purpose: Cleans and formats scraped data

   Important Methods:

   a) clean_contact_data(raw_data)
      Parameters: raw_data (dictionary) - Raw scraped data
      Returns: Cleaned dictionary
      Functionality: Removes duplicates, validates emails, formats phone numbers
      
   b) validate_email(email_string)
      Parameters: email_string (string) - Email to validate
      Returns: Boolean (True if valid format)
      Functionality: Uses regex to check email format
      
   c) format_phone(phone_string)
      Parameters: phone_string (string) - Raw phone number
      Returns: Formatted phone string
      Functionality: Removes special characters, standardizes format
      
   d) remove_duplicates(data_list)
      Parameters: data_list (list) - List of contact dictionaries
      Returns: List without duplicates
      Functionality: Compares entries, keeps unique records
      
   e) structure_response(cleaned_data)
      Parameters: cleaned_data (list) - Processed data
      Returns: Formatted JSON response
      Functionality: Wraps data in response structure with metadata

================================================================================

4. APP.PY
   Purpose: Flask backend API that ties everything together

   Important Methods:

   a) create_app()
      Parameters: None
      Returns: Flask application object
      Functionality: Initializes Flask app with routes and error handlers
      
   b) route_search() [GET/POST /api/search]
      Parameters: search_term (from request body)
      Returns: JSON response with contacts
      Functionality: Calls scraper.py methods, returns structured data
      
   c) route_status() [GET /api/status]
      Parameters: None
      Returns: JSON with scraper status
      Functionality: Returns health check and rate limit info
      
   d) error_handler(error)
      Parameters: error (Exception object)
      Returns: JSON error response
      Functionality: Catches exceptions, returns friendly error messages
      
   e) run_app(host, port, debug)
      Parameters: host (string), port (int), debug (boolean)
      Returns: None
      Functionality: Starts Flask development server

================================================================================

5. INDEX.HTML
   Purpose: Frontend user interface

   Structure:
   - Search input field
   - Submit button
   - Results display area
   - Loading spinner
   - Error message container

   Key Elements:
   - Input ID: search_box
   - Button ID: search_btn
   - Results Container ID: results_container

================================================================================

6. SCRIPT.JS
   Purpose: Frontend logic and API communication

   Important Methods:

   a) handleSearch(event)
      Parameters: event (DOM event)
      Returns: None
      Functionality: Triggers on button click, calls fetchResults()
      
   b) fetchResults(searchTerm)
      Parameters: searchTerm (string) - User input
      Returns: Promise with API response
      Functionality: Makes POST request to /api/search endpoint
      
   c) displayResults(data)
      Parameters: data (JSON object) - API response
      Returns: None
      Functionality: Renders contact cards in HTML
      
   d) displayError(errorMessage)
      Parameters: errorMessage (string) - Error text
      Returns: None
      Functionality: Shows error notification to user
      
   e) formatContact(contact)
      Parameters: contact (object) - Single contact data
      Returns: HTML string
      Functionality: Converts contact to HTML card format

================================================================================
RUNNING COMMANDS
================================================================================

Step 1: Install Dependencies
Command: pip install -r backend/requirements.txt

Step 2: Start Backend Server
Command: cd backend && python app.py
Expected Output: WARNING in app.run() is not intended for production use. Running on http://127.0.0.1:5000

Step 3: Open Frontend
Command: Open index.html in web browser or serve it via Python
Command: python -m http.server 8000
Access: http://localhost:8000

Step 4: Test the Application
Action: Type "restaurants in coimbatore" in search box
Action: Click Search button
Observe: Results load and display contact information

================================================================================
OUTPUT EXAMPLE
================================================================================

User Input: "top restaurants in coimbatore"

API Response (JSON):
{
  "status": "success",
  "search_term": "top restaurants in coimbatore",
  "results_count": 10,
  "data": [
    {
      "business_name": "ABC Restaurant",
      "email": "contact@abcrestaurant.com",
      "phone": "+91-9876543210",
      "website": "www.abcrestaurant.com",
      "source_url": "https://maps.google.com/..."
    },
    {
      "business_name": "XYZ Cafe",
      "email": "info@xyzcafe.com",
      "phone": "+91-9123456789",
      "website": "www.xyzcafe.com",
      "source_url": "https://maps.google.com/..."
    }
  ],
  "timestamp": "2025-12-18T19:53:00Z"
}

Frontend Display:
- Card showing business name
- Contact email (clickable)
- Phone number (clickable to call)
- Website link
- Total count: 10 results found

================================================================================
KEY LEARNING POINTS
================================================================================

1. Selenium automates browser actions like a human would
2. BeautifulSoup parses HTML structure to extract data
3. Regex finds patterns like emails and phone numbers
4. APIs are faster than scraping when available
5. Rate limiting protects servers and your scraper
6. Error handling prevents crashes mid-scrape
7. Data validation ensures quality output

================================================================================
ETHICAL CONSIDERATIONS
================================================================================

Always Remember:
- Check if site allows scraping (robots.txt, ToS)
- Use delays between requests (respect server resources)
- Respect 429 (Too Many Requests) responses

================================================================================