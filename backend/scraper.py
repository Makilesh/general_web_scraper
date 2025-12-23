"""
Web Scraper Module - Educational Project
Uses Selenium and BeautifulSoup to scrape publicly available data
IMPORTANT: Only use on sources that permit scraping. Check robots.txt and ToS.
"""

import re
import time
from urllib.parse import urljoin, urlparse
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


def scrape_google_maps_page(url):
    """
    Scrapes Google Maps business page to get business info and website URL

    Parameters:
        url (string): Google Maps URL

    Returns:
        Dictionary with business info from Google Maps
    """
    driver = None
    try:
        driver = initialize_driver()
        driver.get(url)

        # Wait for page to load
        time.sleep(3)

        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # Extract business name
        business_name = None
        try:
            name_element = soup.find('h1')
            if name_element:
                business_name = name_element.get_text(strip=True)
        except:
            pass

        # Extract phone from Google Maps
        phone = None
        try:
            # Look for phone patterns in buttons or divs with aria-label
            phone_pattern = r'(\+91[-\s]?)?[6-9]\d{9}'
            phones = re.findall(phone_pattern, page_source)
            if phones:
                phone = phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
        except:
            pass

        # Extract website URL from Google Maps
        website = None
        try:
            # Look for website link (usually has data-item-id="authority" or similar)
            website_links = soup.find_all('a', href=True)
            for link in website_links:
                href = link.get('href', '')
                # Filter out Google/social media links
                if (href.startswith('http') and 
                    'google.com' not in href and 
                    'facebook.com' not in href and 
                    'instagram.com' not in href and
                    'twitter.com' not in href and
                    'youtube.com' not in href):
                    website = href
                    break
        except:
            pass

        return {
            'business_name': business_name,
            'phone': phone,
            'website': website,
            'maps_url': url
        }

    except Exception as e:
        print(f"Error scraping Google Maps page {url}: {e}")
        return {
            'business_name': None,
            'phone': None,
            'website': None,
            'maps_url': url
        }
    finally:
        if driver:
            driver.quit()


def scrape_single_page(url, driver=None):
    """
    Opens business website URL with Selenium and scrapes for contact info

    Parameters:
        url (string): Business website to scrape
        driver: Optional existing WebDriver instance

    Returns:
        Dictionary with email and additional contact details
    """
    close_driver = False
    if driver is None:
        driver = initialize_driver()
        close_driver = True
    
    try:
        driver.get(url)
        time.sleep(2)
        
        # Get page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')

        # Extract contact info from main page
        contact_info = extract_contact_info_from_website(page_source, soup)
        
        # If no email found, try to find and visit contact/about pages
        if not contact_info.get('email'):
            contact_pages = find_contact_pages(soup, url)
            for contact_url in contact_pages[:2]:  # Try first 2 contact pages
                try:
                    print(f"    Checking contact page: {contact_url}")
                    driver.get(contact_url)
                    time.sleep(1)
                    contact_page_source = driver.page_source
                    contact_soup = BeautifulSoup(contact_page_source, 'lxml')
                    additional_info = extract_contact_info_from_website(contact_page_source, contact_soup)
                    
                    if additional_info.get('email'):
                        contact_info['email'] = additional_info['email']
                        break
                    if additional_info.get('phone') and not contact_info.get('phone'):
                        contact_info['phone'] = additional_info['phone']
                except Exception as e:
                    print(f"    Error checking contact page: {e}")
                    continue

        contact_info['website'] = url
        return contact_info

    except Exception as e:
        print(f"Error scraping website {url}: {e}")
        return {
            'email': None,
            'phone': None,
            'website': url
        }
    finally:
        if close_driver and driver:
            driver.quit()


def find_contact_pages(soup, base_url):
    """
    Finds links to contact, about, or other pages that might contain email

    Parameters:
        soup: BeautifulSoup object
        base_url: Base URL of the website

    Returns:
        List of URLs to check
    """
    contact_pages = []
    contact_keywords = ['contact', 'about', 'reach', 'get-in-touch', 'connect', 'support']
    
    try:
        # Parse base URL to get domain
        base_domain = urlparse(base_url).netloc
        
        # Find all links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href', '').lower()
            text = link.get_text(strip=True).lower()
            
            # Check if link text or href contains contact keywords
            if any(keyword in href or keyword in text for keyword in contact_keywords):
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, link['href'])
                
                # Only include URLs from same domain
                if urlparse(full_url).netloc == base_domain:
                    contact_pages.append(full_url)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_pages = []
        for page in contact_pages:
            if page not in seen:
                seen.add(page)
                unique_pages.append(page)
        
        return unique_pages[:3]  # Return max 3 contact pages
    
    except Exception as e:
        print(f"    Error finding contact pages: {e}")
        return []


def extract_contact_info_from_website(page_source, soup=None):
    """
    Enhanced extraction - Uses multiple methods to find emails and phones

    Parameters:
        page_source (string): HTML content of business website
        soup: BeautifulSoup object (optional, will create if not provided)

    Returns:
        Dictionary with contact details
    """
    if soup is None:
        soup = BeautifulSoup(page_source, 'lxml')

    email = None
    phone = None

    # Method 1: Look for mailto: links (most reliable)
    try:
        mailto_links = soup.find_all('a', href=re.compile(r'mailto:', re.I))
        for link in mailto_links:
            href = link.get('href', '')
            email_match = re.search(r'mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', href, re.I)
            if email_match:
                email = email_match.group(1).lower()
                break
    except:
        pass

    # Method 2: Look in specific elements (footer, contact sections)
    if not email:
        try:
            # Check footer, contact divs, etc.
            contact_sections = soup.find_all(['footer', 'div'], class_=re.compile(r'(contact|footer|email)', re.I))
            for section in contact_sections:
                section_text = section.get_text()
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, section_text, re.I)
                
                # Filter out common non-business emails
                excluded_patterns = ['example.com', 'domain.com', 'email.com', 'test.com', 'wix.com', 'sitelock.com', 'placeholder']
                valid_emails = [e for e in emails if not any(pattern in e.lower() for pattern in excluded_patterns)]
                
                if valid_emails:
                    email = valid_emails[0].lower()
                    break
        except:
            pass

    # Method 3: General page source regex search
    if not email:
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, page_source, re.I)
            
            # Filter out common non-business emails and image file patterns
            excluded_patterns = ['example.com', 'domain.com', 'email.com', 'test.com', 'wix.com', 
                               'sitelock.com', 'schema.org', 'w3.org', 'placeholder', '@2x.png', '@3x.png']
            valid_emails = [e for e in emails if not any(pattern in e.lower() for pattern in excluded_patterns)]
            
            if valid_emails:
                email = valid_emails[0].lower()
        except:
            pass

    # Extract phone number using multiple methods
    try:
        # Method 1: Look for tel: links
        tel_links = soup.find_all('a', href=re.compile(r'tel:', re.I))
        for link in tel_links:
            href = link.get('href', '')
            phone_digits = re.sub(r'\D', '', href)
            if len(phone_digits) >= 10:
                phone = phone_digits
                break
    except:
        pass

    # Method 2: Multiple phone patterns
    if not phone:
        try:
            # Look in contact sections first
            contact_sections = soup.find_all(['footer', 'div'], class_=re.compile(r'(contact|footer|phone|tel)', re.I))
            search_text = ' '.join([section.get_text() for section in contact_sections]) if contact_sections else page_source
            
            phone_patterns = [
                r'(\+91[-\s]?)?[6-9]\d{9}',  # Indian mobile
                r'\+91[-.\s]?\d{10}',  # With country code
                r'[6-9]\d{2}[-.\s]?\d{3}[-.\s]?\d{4}',  # With separators
            ]
            
            for pattern in phone_patterns:
                phones = re.findall(pattern, search_text)
                if phones:
                    phone_str = phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
                    phone = re.sub(r'\D', '', phone_str)
                    if len(phone) >= 10:
                        break
        except:
            pass

    return {
        'email': email,
        'phone': phone
    }


def scrape_all_results(maps_urls_list):
    """
    Loops through Google Maps URLs, extracts business info and website,
    then scrapes the actual business website for email/phone

    Parameters:
        maps_urls_list (list): List of Google Maps URLs to scrape

    Returns:
        List of dictionaries with complete contact info
    """
    results = []

    for idx, maps_url in enumerate(maps_urls_list, 1):
        print(f"Processing {idx}/{len(maps_urls_list)}: {maps_url}")

        # Step 1: Get business info from Google Maps
        maps_data = scrape_google_maps_page(maps_url)
        
        business_name = maps_data.get('business_name')
        phone_from_maps = maps_data.get('phone')
        website = maps_data.get('website')
        
        print(f"  Business: {business_name}")
        print(f"  Phone from Maps: {phone_from_maps}")
        print(f"  Website: {website}")

        # Step 2: If website exists, scrape it for email and additional contact info
        email = None
        phone_from_website = None
        
        if website:
            try:
                print(f"  Scraping website: {website}")
                website_data = scrape_single_page(website)
                email = website_data.get('email')
                phone_from_website = website_data.get('phone')
                print(f"  Email found: {email}")
                print(f"  Phone from website: {phone_from_website}")
            except Exception as e:
                print(f"  Error scraping website: {e}")

        # Combine data - prefer phone from website, fallback to Maps
        final_phone = phone_from_website or phone_from_maps

        result = {
            'business_name': business_name,
            'email': email,
            'phone': final_phone,
            'website': website,
            'source_url': maps_url
        }
        
        results.append(result)

        # Rate limiting - be respectful
        time.sleep(2)

    return results

