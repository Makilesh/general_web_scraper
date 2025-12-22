"""
Data Processing Module - Educational Project
Cleans and formats scraped data
"""

import re
from datetime import datetime


def validate_email(email_string):
    """
    Uses regex to check email format

    Parameters:
        email_string (string): Email to validate

    Returns:
        Boolean (True if valid format)
    """
    if not email_string:
        return False

    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return bool(re.match(email_pattern, email_string))


def format_phone(phone_string):
    """
    Removes special characters, standardizes format

    Parameters:
        phone_string (string): Raw phone number

    Returns:
        Formatted phone string
    """
    if not phone_string:
        return None

    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone_string)

    # Format for Indian numbers (10 digits)
    if len(digits) == 10:
        return f"+91-{digits}"
    elif len(digits) == 12 and digits.startswith('91'):
        return f"+{digits[:2]}-{digits[2:]}"
    elif len(digits) > 10:
        # Return with country code
        return f"+{digits[:2]}-{digits[2:]}"
    else:
        return phone_string


def clean_contact_data(raw_data):
    """
    Removes duplicates, validates emails, formats phone numbers

    Parameters:
        raw_data (dictionary): Raw scraped data

    Returns:
        Cleaned dictionary
    """
    cleaned = {}

    # Clean business name
    cleaned['business_name'] = raw_data.get('business_name', 'N/A')
    if cleaned['business_name']:
        cleaned['business_name'] = cleaned['business_name'].strip()

    # Validate and clean email
    email = raw_data.get('email')
    if email and validate_email(email):
        cleaned['email'] = email.strip().lower()
    else:
        cleaned['email'] = None

    # Format phone number
    phone = raw_data.get('phone')
    cleaned['phone'] = format_phone(phone)

    # Clean website URL
    website = raw_data.get('website')
    if website:
        cleaned['website'] = website.strip()
    else:
        cleaned['website'] = None

    # Keep source URL
    cleaned['source_url'] = raw_data.get('source_url', '')

    return cleaned


def remove_duplicates(data_list):
    """
    Compares entries, keeps unique records

    Parameters:
        data_list (list): List of contact dictionaries

    Returns:
        List without duplicates
    """
    seen = set()
    unique_data = []

    for item in data_list:
        # Create a unique identifier using business name or email or phone
        identifier = (
            item.get('business_name', '').lower(),
            item.get('email', ''),
            item.get('phone', '')
        )

        # Skip if all fields are empty
        if not any(identifier):
            continue

        # Check if we've seen this combination before
        if identifier not in seen:
            seen.add(identifier)
            unique_data.append(item)

    return unique_data


def structure_response(cleaned_data, search_term=""):
    """
    Wraps data in response structure with metadata

    Parameters:
        cleaned_data (list): Processed data
        search_term (string): Original search term

    Returns:
        Formatted JSON response
    """
    response = {
        "status": "success",
        "search_term": search_term,
        "results_count": len(cleaned_data),
        "data": cleaned_data,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    return response


def process_scraped_data(raw_data_list, search_term=""):
    """
    Main processing pipeline that combines all cleaning steps

    Parameters:
        raw_data_list (list): List of raw scraped dictionaries
        search_term (string): Original search term

    Returns:
        Structured JSON response
    """
    # Step 1: Clean each contact
    cleaned_list = [clean_contact_data(item) for item in raw_data_list]

    # Step 2: Remove duplicates
    unique_list = remove_duplicates(cleaned_list)

    # Step 3: Filter out entries with no contact information
    valid_list = [
        item for item in unique_list
        if item.get('email') or item.get('phone') or item.get('website')
    ]

    # Step 4: Structure response
    response = structure_response(valid_list, search_term)

    return response
