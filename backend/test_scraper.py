"""
Quick test to debug email extraction
"""
import scraper

# Test the fast scraping method on one of the websites
test_url = "http://appathaasamayall.com/"

print(f"Testing email extraction from: {test_url}\n")

# Try fast method
print("=== Testing Fast Method (requests) ===")
result = scraper.scrape_with_requests(test_url)
print(f"Email: {result.get('email')}")
print(f"Phone: {result.get('phone')}")

# Try another URL
test_url2 = "https://cockraco.com/"
print(f"\n\nTesting email extraction from: {test_url2}\n")
result2 = scraper.scrape_with_requests(test_url2)
print(f"Email: {result2.get('email')}")
print(f"Phone: {result2.get('phone')}")
