# Web Scraper - Educational Project

A full-stack web scraper application that demonstrates how to extract business contact information using BeautifulSoup and Selenium.

## ⚠️ IMPORTANT DISCLAIMER

**This project is for educational purposes only.** This tool demonstrates web scraping techniques using BeautifulSoup and Selenium to scrape publicly available data from sources that permit scraping.

**Always:**
- Check `robots.txt` before scraping any website
- Review the website's Terms of Service
- Respect rate limits and server resources
- Only use on sources that explicitly permit scraping
- Add delays between requests to avoid overwhelming servers

## 📋 Project Overview

This web scraper accepts a search term from the user, fetches relevant business results from Google Maps, and extracts contact information including:
- Business names
- Email addresses
- Phone numbers
- Website URLs

**Example:** User inputs "restaurants in coimbatore" → System fetches top 10 results → Extracts contact details → Returns formatted data.

## 🎯 Learning Objectives

This project demonstrates:
- Browser automation with Selenium WebDriver
- HTML parsing with BeautifulSoup
- Handling asynchronous content loading
- Data extraction and validation with regex
- Building RESTful APIs with Flask
- Creating responsive web interfaces
- Processing and structuring scraped data

## 📁 Project Structure

```
project_root/
│
├── backend/
│   ├── requirements.txt       # Python dependencies
│   ├── scraper.py             # Core scraping logic
│   ├── data_processor.py      # Data cleaning and formatting
│   └── app.py                 # Flask API server
│
├── frontend/
│   ├── index.html             # User interface
│   ├── style.css              # Styling
│   └── script.js              # Frontend logic
│
├── web_scraper_guide.md       # Detailed specification
└── README.md                  # This file
```

## 🛠️ Technologies Used

### Backend
- **Python 3.8+**
- **Selenium 4.0+** - Browser automation
- **BeautifulSoup 4.9+** - HTML parsing
- **Flask 2.0+** - Web framework
- **Requests 2.25+** - HTTP library
- **lxml 4.6+** - XML/HTML processing

### Frontend
- **HTML5**
- **CSS3**
- **Vanilla JavaScript**
- **Fetch API** - HTTP requests

## 📥 Installation

### Prerequisites

1. **Python 3.8 or higher** installed on your system
2. **Google Chrome** browser installed
3. **ChromeDriver** compatible with your Chrome version (Selenium will handle this automatically with recent versions)

### Step 1: Clone or Download the Project

```bash
cd D:\Shamla_tech\general_scraper
```

### Step 2: Install Python Dependencies

```bash
pip install -r backend/requirements.txt
```

This will install:
- selenium
- beautifulsoup4
- requests
- flask
- flask-cors
- python-dotenv
- lxml

### Step 3: Verify Installation

Check that all packages are installed:

```bash
pip list | findstr "selenium beautifulsoup4 flask"
```

## 🚀 Running the Application

### Step 1: Start the Backend Server

Open a terminal/command prompt and run:

```bash
cd backend
python app.py
```

You should see output like:

```
Starting Web Scraper API on http://127.0.0.1:5000
IMPORTANT: This is for educational purposes only.
Always check robots.txt and Terms of Service before scraping.
 * Running on http://127.0.0.1:5000
```

Keep this terminal window open.

### Step 2: Open the Frontend

**Option A: Direct File Opening**
1. Navigate to the `frontend` folder
2. Double-click `index.html` to open it in your web browser

**Option B: Using Python HTTP Server** (Recommended)

Open a new terminal/command prompt and run:

```bash
cd frontend
python -m http.server 8000
```

Then open your browser and go to:
```
http://localhost:8000
```

## 📖 How to Use

1. **Open the web interface** in your browser
2. **Enter a search term** in the search box (e.g., "restaurants in coimbatore")
3. **Click the Search button** or press Enter
4. **Wait for results** - The scraper will:
   - Search Google Maps for matching businesses
   - Visit each result page
   - Extract contact information
   - Clean and format the data
5. **View results** displayed as cards with contact details

### Example Search Terms

- "restaurants in coimbatore"
- "hotels in chennai"
- "cafes in bangalore"
- "gyms in mumbai"
- "bookstores in delhi"

## 🏗️ Architecture

### Backend Components

#### 1. `scraper.py`
Core scraping module with methods:
- `initialize_driver()` - Sets up headless Chrome browser
- `search_business_directory(search_term)` - Fetches URLs from Google Maps
- `scrape_single_page(url)` - Extracts data from one page
- `extract_contact_info(page_source)` - Parses HTML for contact details
- `scrape_all_results(urls_list)` - Processes multiple URLs

#### 2. `data_processor.py`
Data cleaning module with methods:
- `validate_email(email_string)` - Checks email format
- `format_phone(phone_string)` - Standardizes phone numbers
- `clean_contact_data(raw_data)` - Cleans individual records
- `remove_duplicates(data_list)` - Removes duplicate entries
- `structure_response(cleaned_data)` - Formats final JSON response

#### 3. `app.py`
Flask API server with endpoints:
- `POST /api/search` - Main search and scrape endpoint
- `GET /api/status` - Health check endpoint
- `GET /` - API information

### Frontend Components

#### 1. `index.html`
User interface with:
- Search input field (`search_box`)
- Search button (`search_btn`)
- Loading spinner
- Results container
- Error display

#### 2. `script.js`
Frontend logic with methods:
- `handleSearch(event)` - Processes search action
- `fetchResults(searchTerm)` - Makes API calls
- `displayResults(data)` - Renders results
- `formatContact(contact)` - Creates HTML cards
- `displayError(message)` - Shows error messages

#### 3. `style.css`
Modern, responsive styling with:
- Clean card-based layout
- Smooth animations
- Mobile-responsive design
- Accessible color scheme

## 📊 API Response Format

```json
{
  "status": "success",
  "search_term": "restaurants in coimbatore",
  "results_count": 10,
  "data": [
    {
      "business_name": "ABC Restaurant",
      "email": "contact@abcrestaurant.com",
      "phone": "+91-9876543210",
      "website": "www.abcrestaurant.com",
      "source_url": "https://www.google.com/maps/place/..."
    }
  ],
  "timestamp": "2025-12-18T19:53:00Z"
}
```

## 🔧 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed: `python --version`
- Check all dependencies are installed: `pip list`
- Try reinstalling requirements: `pip install -r backend/requirements.txt`

### ChromeDriver errors
- Update Selenium: `pip install --upgrade selenium`
- Ensure Chrome browser is installed
- Modern Selenium versions auto-manage ChromeDriver

### Frontend can't connect to backend
- Verify backend is running on http://127.0.0.1:5000
- Check `API_BASE_URL` in `script.js` matches your backend
- Look for CORS errors in browser console (flask-cors should handle this)

### No results returned
- Check your internet connection
- Try a different search term
- The search term should be location-specific
- Google Maps may have rate-limited your IP (wait and try again)

### Slow performance
- Scraping takes time (10 results ≈ 30-60 seconds)
- Each page load includes intentional delays to be respectful
- Consider reducing the number of results in `scraper.py`

## 🔒 Ethical Considerations

### Always Remember

1. **Check robots.txt**: Before scraping any site, check `https://example.com/robots.txt`
2. **Read Terms of Service**: Some websites explicitly prohibit scraping
3. **Use delays**: The code includes `time.sleep()` to avoid overwhelming servers
4. **Respect 429 responses**: If you get "Too Many Requests," stop and wait
5. **Use APIs when available**: They're faster, more reliable, and legal
6. **Don't scrape personal data**: Only collect publicly available business information
7. **Educational use only**: This project is for learning, not commercial use

## 📚 Key Learning Points

1. **Selenium** automates browser interactions like a human user
2. **BeautifulSoup** parses HTML structure to extract specific data
3. **Regex patterns** identify emails, phone numbers, and other patterns
4. **APIs** provide structured data and are preferred over scraping
5. **Rate limiting** protects both the target server and your scraper
6. **Error handling** prevents crashes during long scraping sessions
7. **Data validation** ensures output quality and reliability

## 🎓 Extension Ideas

Want to learn more? Try extending this project:

- Add export to CSV/Excel functionality
- Implement pagination for more results
- Add filters (by rating, type, etc.)
- Create a database to store scraped data
- Add user authentication
- Implement caching to avoid re-scraping
- Add support for multiple search engines
- Create a scheduling system for automated scraping

## 📄 License

This project is for educational purposes only. Use responsibly and ethically.

## 🤝 Contributing

This is an educational project. Feel free to fork and modify for your learning.

## ⚖️ Legal Notice

The developers of this project are not responsible for misuse of this tool. Users must:
- Comply with all applicable laws and regulations
- Respect website Terms of Service
- Only scrape data they have permission to collect
- Use the tool responsibly and ethically

---

**Built with Flask, Selenium, and BeautifulSoup for educational purposes.**

**Always respect website ToS and robots.txt** 🤖
