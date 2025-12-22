"""
Web Scraper Module - Educational Project
Uses Selenium and BeautifulSoup to scrape publicly available data
IMPORTANT: Only use on sources that permit scraping. Check robots.txt and ToS.
"""

import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests


def initialize_driver():
    """
    Sets up Chrome WebDriver with options for headless browsing

    Returns:
        WebDriver object configured for scraping
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        print(f"Error initializing driver: {e}")
        raise


def search_business_directory(search_term):
    """
    Uses Google Maps to fetch business result URLs

    Parameters:
        search_term (string): What to search for (e.g., "restaurants in coimbatore")

    Returns:
        List of URLs containing results
    """
    driver = None
    try:
        driver = initialize_driver()

        # Construct Google Maps search URL
        encoded_term = search_term.replace(' ', '+')
        search_url = f"https://www.google.com/maps/search/{encoded_term}"

        driver.get(search_url)

        # Wait for results to load
        time.sleep(3)

        # Scroll to load more results
        scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
        for _ in range(3):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
            time.sleep(1)

        # Extract business links
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # Find business links (this is a simplified approach)
        links = []
        results = soup.find_all('a', href=re.compile(r'/maps/place/'))

        for result in results[:10]:  # Limit to top 10
            href = result.get('href')
            if href and 'https' not in href:
                full_url = f"https://www.google.com{href}"
                links.append(full_url)
            elif href:
                links.append(href)

        # Remove duplicates
        unique_links = list(set(links))[:10]

        return unique_links

    except Exception as e:
        print(f"Error searching business directory: {e}")
        return []
    finally:
        if driver:
            driver.quit()


def scrape_single_page(url):
    """
    Opens URL with Selenium, waits for content, parses HTML

    Parameters:
        url (string): Website to scrape

    Returns:
        Dictionary with name, email, phone
    """
    driver = None
    try:
        driver = initialize_driver()
        driver.get(url)

        # Wait for page to load
        time.sleep(2)

        # Get page source
        page_source = driver.page_source

        # Extract contact info
        contact_info = extract_contact_info(page_source)
        contact_info['source_url'] = url

        return contact_info

    except Exception as e:
        print(f"Error scraping page {url}: {e}")
        return {
            'business_name': None,
            'email': None,
            'phone': None,
            'website': None,
            'source_url': url
        }
    finally:
        if driver:
            driver.quit()


def extract_contact_info(page_source):
    """
    Uses regex and BeautifulSoup to find emails, phones, names

    Parameters:
        page_source (string): HTML content

    Returns:
        Dictionary with contact details
    """
    soup = BeautifulSoup(page_source, 'lxml')

    # Extract business name
    business_name = None
    name_selectors = [
        'h1',
        {'class': re.compile(r'(title|name|heading)', re.I)},
        {'itemprop': 'name'}
    ]
    for selector in name_selectors:
        element = soup.find(selector) if isinstance(selector, str) else soup.find(attrs=selector)
        if element:
            business_name = element.get_text(strip=True)
            break

    # Extract email using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, page_source)
    email = emails[0] if emails else None

    # Extract phone number using regex
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, page_source)
    phone = ''.join(phones[0]) if phones else None

    # Alternative phone extraction
    if not phone:
        phone_pattern2 = r'(\+91[-\s]?)?[6-9]\d{9}'
        phones2 = re.findall(phone_pattern2, page_source)
        phone = phones2[0] if phones2 else None

    # Extract website
    website = None
    website_links = soup.find_all('a', href=re.compile(r'http'))
    for link in website_links:
        href = link.get('href')
        if href and 'google.com' not in href and 'facebook.com' not in href:
            website = href
            break

    return {
        'business_name': business_name,
        'email': email,
        'phone': phone,
        'website': website
    }


def scrape_all_results(urls_list):
    """
    Loops through URLs, calls scrape_single_page for each

    Parameters:
        urls_list (list): List of URLs to scrape

    Returns:
        List of dictionaries with contact info
    """
    results = []

    for idx, url in enumerate(urls_list, 1):
        print(f"Scraping {idx}/{len(urls_list)}: {url}")

        contact_data = scrape_single_page(url)
        results.append(contact_data)

        # Rate limiting - be respectful
        time.sleep(2)

    return results
