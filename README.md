# Proxy Management and URL Generation Script

This Python script provides a simple way to manage proxies and generate URLs from a predefined list.
For security reasons, this is just a snippet, without using the functions.

## Features

- **Change Proxy**: Fetches proxy data from a Google Sheets document and sets the `http_proxy` and `https_proxy` environment variables.
- **Generate URL**: Randomly selects a region from a list in a JSON file and generates a URL by appending a random number within a specified range.
- **Get Data**: Fetches data from a generated URL and extracts specific company information such as name, address, and contact details using BeautifulSoup.

## Requirements

- Python 3.x
- Google Sheets API credentials (`credentials.json`)
- Required Python libraries:
  - `google-api-python-client`
  - `google-auth-httplib2`
  - `google-auth-oauthlib`
  - `requests`
  - `beautifulsoup4`

## Setup

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/repositoryname.git
    cd repositoryname
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Google Sheets API credentials:
    - Follow the [Google Sheets API Quickstart](https://developers.google.com/sheets/api/quickstart/python) to generate `credentials.json` and save it to your project directory.

4. Run the script:
    ```bash
    python find_companies.py
    ```

## Usage

- **change_proxy()**: Changes the proxy settings by selecting a random proxy from the Google Sheet.
- **generate_url()**: Generates a URL using data from a JSON file and appends a random number.
- **get_data_from(url)**: Fetches and parses company data from a given URL.
