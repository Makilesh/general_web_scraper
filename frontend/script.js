/**
 * Web Scraper Frontend - Educational Project
 * Handles user interactions and API communication
 */

// Configuration
const API_BASE_URL = 'http://127.0.0.1:5000';

// DOM Elements
const searchBox = document.getElementById('search_box');
const searchBtn = document.getElementById('search_btn');
const loadingSpinner = document.getElementById('loading_spinner');
const errorContainer = document.getElementById('error_container');
const errorMessage = document.getElementById('error_message');
const resultsContainer = document.getElementById('results_container');
const resultsHeader = document.getElementById('results_header');
const resultsCount = document.getElementById('results_count');
const resultsList = document.getElementById('results_list');

// Event Listeners
searchBtn.addEventListener('click', handleSearch);
searchBox.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch(e);
    }
});

/**
 * Triggers on button click, calls fetchResults()
 *
 * @param {Event} event - DOM event
 */
function handleSearch(event) {
    event.preventDefault();

    const searchTerm = searchBox.value.trim();

    if (!searchTerm) {
        displayError('Please enter a search term');
        return;
    }

    // Get selected search method
    const searchMethod = document.querySelector('input[name="search_method"]:checked').value;

    // Reset UI
    hideError();
    hideResults();
    showLoading();

    // Fetch results with selected method
    fetchResults(searchTerm, searchMethod);
}

/**
 * Makes POST request to appropriate API endpoint based on search method
 *
 * @param {string} searchTerm - User input
 * @param {string} method - 'google' or 'maps'
 * @returns {Promise} Promise with API response
 */
async function fetchResults(searchTerm, method = 'google') {
    try {
        // Choose endpoint based on method
        const endpoint = method === 'google' ? '/api/search-google' : '/api/search';
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                search_term: searchTerm
            })
        });

        const data = await response.json();

        hideLoading();

        if (response.ok && data.status === 'success') {
            if (data.results_count === 0) {
                displayError('No results found. Try a different search term.');
            } else {
                displayResults(data);
            }
        } else {
            displayError(data.message || 'An error occurred while fetching results');
        }

    } catch (error) {
        hideLoading();
        console.error('Fetch error:', error);
        displayError('Failed to connect to the server. Make sure the backend is running on http://127.0.0.1:5000');
    }
}

/**
 * Renders contact cards in HTML
 *
 * @param {Object} data - API response
 */
function displayResults(data) {
    // Update results count
    resultsCount.textContent = `${data.results_count} result${data.results_count !== 1 ? 's' : ''} found`;

    // Clear previous results
    resultsList.innerHTML = '';

    // Create contact cards
    data.data.forEach(contact => {
        const card = formatContact(contact);
        resultsList.innerHTML += card;
    });

    // Show results
    resultsHeader.classList.remove('hidden');
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Converts contact to HTML card format
 *
 * @param {Object} contact - Single contact data
 * @returns {string} HTML string
 */
function formatContact(contact) {
    const businessName = contact.business_name || 'Business Name Not Available';
    const email = contact.email;
    const phone = contact.phone;
    const website = contact.website;
    const sourceUrl = contact.source_url;

    return `
        <div class="contact-card">
            <h3>${escapeHtml(businessName)}</h3>
            <div class="contact-info">
                ${email ? `
                    <div class="contact-item">
                        <span class="icon">📧</span>
                        <a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a>
                    </div>
                ` : `
                    <div class="contact-item no-data">
                        <span class="icon">📧</span>
                        <span>Email not available</span>
                    </div>
                `}

                ${phone ? `
                    <div class="contact-item">
                        <span class="icon">📞</span>
                        <a href="tel:${escapeHtml(phone)}">${escapeHtml(phone)}</a>
                    </div>
                ` : `
                    <div class="contact-item no-data">
                        <span class="icon">📞</span>
                        <span>Phone not available</span>
                    </div>
                `}

                ${website ? `
                    <div class="contact-item">
                        <span class="icon">🌐</span>
                        <a href="${escapeHtml(website)}" target="_blank" rel="noopener noreferrer">
                            ${escapeHtml(truncateUrl(website))}
                        </a>
                    </div>
                ` : `
                    <div class="contact-item no-data">
                        <span class="icon">🌐</span>
                        <span>Website not available</span>
                    </div>
                `}
            </div>

            ${sourceUrl ? `
                <div class="source-link">
                    <a href="${escapeHtml(sourceUrl)}" target="_blank" rel="noopener noreferrer">
                        View Source →
                    </a>
                </div>
            ` : ''}
        </div>
    `;
}

/**
 * Shows error notification to user
 *
 * @param {string} message - Error text
 */
function displayError(message) {
    errorMessage.textContent = message;
    errorContainer.classList.remove('hidden');
}

/**
 * Hides error notification
 */
function hideError() {
    errorContainer.classList.add('hidden');
}

/**
 * Closes error notification (called from HTML)
 */
function closeError() {
    hideError();
}

/**
 * Shows loading spinner
 */
function showLoading() {
    loadingSpinner.classList.remove('hidden');
}

/**
 * Hides loading spinner
 */
function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

/**
 * Hides results section
 */
function hideResults() {
    resultsHeader.classList.add('hidden');
    resultsList.innerHTML = '';
}

/**
 * Escapes HTML to prevent XSS
 *
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Truncates long URLs for display
 *
 * @param {string} url - URL to truncate
 * @returns {string} Truncated URL
 */
function truncateUrl(url) {
    if (!url) return '';
    const maxLength = 40;
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// Initial status check
fetch(`${API_BASE_URL}/api/status`)
    .then(response => response.json())
    .then(data => {
        console.log('API Status:', data);
    })
    .catch(error => {
        console.warn('Could not connect to API. Make sure the backend is running.');
    });
