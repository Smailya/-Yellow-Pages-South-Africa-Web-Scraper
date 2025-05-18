import requests
from bs4 import BeautifulSoup
import csv

# Target URL
url = "https://www.yellowpages-south-africa.com/?q=sales"

# Send GET request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
response = requests.get(url, headers=headers)

# Parse HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Find all business listing cards
cards = soup.find_all('div', class_='card')

# List to hold scraped data
results = []

# Loop through each card and extract info
for card in cards:
    business = {
        'name': '',
        'phone': '',
        'whatsapp': '',
        'address': '',
        'email': '',
        'website': ''
    }

    # Business name and link
    header = card.find('div', class_='card-header')
    if header:
        h2 = header.find('h2')
        if h2 and h2.a:
            business['name'] = h2.a.get_text(strip=True)
            business['website'] = h2.a['href']

    # Card body with details
    body = card.find('div', class_='card-body')
    if body:
        rows = body.find_all('div', class_='row mb-2')
        for row in rows:
            label_tag = row.find('div', class_='col-4')
            value_tag = row.find('div', class_='col-8')
            if not label_tag or not value_tag:
                continue

            label = label_tag.get_text(strip=True).lower().rstrip(':')
            value = value_tag.get_text(strip=True)

            if label == 'phone':
                business['phone'] = value
            elif label == 'whatsapp':
                business['whatsapp'] = value
            elif label == 'address':
                business['address'] = value
            elif label == 'email':
                email_span = value_tag.find('span', class_='__cf_email__')
                if email_span and email_span.has_attr('data-cfemail'):
                    business['email'] = '[protected email]'
                else:
                    business['email'] = value
            elif label == 'website':
                a_tag = value_tag.find('a')
                if a_tag and a_tag.has_attr('href'):
                    business['website'] = a_tag['href']

    results.append(business)

# Save results to a neatly structured CSV file
csv_file = 'yellow_pages_data.csv'
fieldnames = ['name', 'phone', 'whatsapp', 'address', 'email', 'website']

# Use UTF-8 with BOM for Excel compatibility
with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Successfully scraped and saved {len(results)} entries to '{csv_file}'")
