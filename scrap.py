import requests
from bs4 import BeautifulSoup

url = "https://www.yellowpages-south-africa.com/search?q=sales"  # Replace with actual search URL if needed
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select("div.container.yellowpages div.card")

results = []

for card in cards:
    business = {}

    # Business name and URL
    header = card.select_one(".card-header h2 a")
    if header:
        business["name"] = header.text.strip()
        business["profile_url"] = header.get("href")

    # Website (usually in the header as well)
    site_link = card.select_one(".card-header a + div a")
    if site_link:
        business["website"] = site_link.get("href")

    # Extract fields from card body
    rows = card.select(".card-body .row.mb-2")
    for row in rows:
        label_el = row.select_one(".col-4 label")
        value_el = row.select_one(".col-8")
        if not label_el or not value_el:
            continue

        label = label_el.text.strip().rstrip(":").lower()
        value = value_el.text.strip()

        # Decode Cloudflare protected email if needed
        email_span = value_el.select_one("span.__cf_email__")
        if email_span and email_span.has_attr("data-cfemail"):
            value = "[email protected]"  # Placeholder (email obfuscated)

        if "phone" in label:
            business["phone"] = value
        elif "whatsapp" in label:
            business["whatsapp"] = value
        elif "email" in label:
            business["email"] = value
        elif "address" in label:
            business["address"] = value
        elif "business hours" in label:
            business["business_hours"] = value

    results.append(business)

# Print results
for biz in results:
    print(biz)
