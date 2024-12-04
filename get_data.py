import os
import json
import random
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup 

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'  # Replace with your spreadsheet ID
RANGE_NAME = 'Sheet1!A:B'  # Range for IP and Port data

def get_proxy_data():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found in the spreadsheet.')
        return None
    
    proxies = []
    for row in values:
        if len(row) >= 2:
            proxies.append({'ip': row[0], 'port': row[1]})
    
    return proxies

def change_proxy():
    proxy_data = get_proxy_data()
    
    if proxy_data:
        # Choose a random proxy
        selected_proxy = random.choice(proxy_data)
        
        proxy = f"{selected_proxy['ip']}:{selected_proxy['port']}"
        
        os.environ['http_proxy'] = f"http://{proxy}"
        os.environ['https_proxy'] = f"https://{proxy}"
        
        # Test if the proxy change works by making a request
        response = requests.get("http://www.google.com")
        if response.status_code == 200:
            print(f"Proxy change to {proxy} was successful!")
        else:
            print(f"Error connecting through {proxy}.")
    else:
        print("No proxy data available.")

def generate_url():
    with open('urls.json', 'r') as file:
        data = json.load(file)
    
    region = random.choice(list(data.keys()))
    urls_data = data[region]
    
    number = random.randint(1, urls_data['range'])
    
    full_url = f"{urls_data['url']}{number}"
    
    return full_url

def get_data_from(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    company_soup = BeautifulSoup(response.text, 'html.parser')
    
    name = company_soup.select_one('table tr:nth-of-type(2) td:nth-of-type(2) h2').text if company_soup.select_one('table tr:nth-of-type(2) td:nth-of-type(2) h2') else None
    street = company_soup.select_one('table tr:nth-of-type(3) td:nth-of-type(2) a').text if company_soup.select_one('table tr:nth-of-type(3) td:nth-of-type(2) a') else None
    postal = company_soup.select_one('table tr:nth-of-type(4) td:nth-of-type(2) h2').text if company_soup.select_one('table tr:nth-of-type(4) td:nth-of-type(2) h2') else None
    telephone = company_soup.select_one('table tr:nth-of-type(6) td:nth-of-type(2)').text if company_soup.select_one('table tr:nth-of-type(6) td:nth-of-type(2)') else None
    email = company_soup.select_one('table tr:nth-of-type(9) td:nth-of-type(2) a').text if company_soup.select_one('table tr:nth-of-type(9) td:nth-of-type(2) a') else None
    
    if name and street and postal and telephone and email:
        return {
            'name': name,
            'street': street,
            'postal': postal,
            'telephone': telephone,
            'email': email
        }
    
    return None
