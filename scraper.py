import requests
from bs4 import BeautifulSoup
import re
import csv

# Define input and output file paths
input_file = 'sites/usefulWebsites2.txt'
output_csv = 'sites/researcher_details.csv'

# Function to robustly extract emails (including Imperial College JS-encoded emails) and phone numbers
def extract_contacts(soup, text):
    emails = set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', text))
    mailto_emails = set(a['href'][7:] for a in soup.select('a[href^="mailto:"]'))
    emails.update(mailto_emails)

    # Imperial College JavaScript-encoded emails
    js_emails = re.findall(r"'([\w.+-]+)'\s*\+\s*'@'\s*\+\s*'([\w.-]+)'", text)
    for parts in js_emails:
        emails.add(parts[0] + '@' + parts[1])

    phones = set(re.findall(r'\+?\d[\d\s()-]{7,}\d', text))
    return emails, phones

# Improved function to extract names with extended filtering
def extract_name(url, soup):
    irrelevant_keywords = ['people', 'researcher', 'faculty', '404', 'error', 'page not found','staff']

    if soup.title:
        title_text = soup.title.get_text(separator=' ', strip=True)
        patterns = [
            r'^(.*?)\s*[|\-•:]',
            r'Profile\s*[|\-•:]\s*(.*?)\s*[|\-•:]',
        ]
        for pattern in patterns:
            match = re.search(pattern, title_text, re.I)
            if match:
                name = match.group(1).strip()
                if (len(name.split()) <= 5 and 
                    not any(kw in name.lower() for kw in irrelevant_keywords) and
                    re.match(r"^[A-Za-z ,.'\-]+$", name)):
                    return name

    name_from_url = url.rstrip('/').split('/')[-1]
    name_from_url = name_from_url.replace('.', ' ').replace('-', ' ').title()
    if (not any(kw in name_from_url.lower() for kw in irrelevant_keywords) and
        re.match(r"^[A-Za-z ,.'\-]+$", name_from_url)):
        return name_from_url

    return 'N/A'

# Match email addresses to researcher names
def match_email_to_name(name, emails):
    name_parts = re.split(r'\s+', name.lower())
    for email in emails:
        email_lower = email.lower()
        if all(part in email_lower for part in name_parts if len(part) > 2):
            return email
    return ', '.join(emails)

# Read URLs from input file
with open(input_file, 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# Open CSV file for writing extracted data
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'URL', 'Emails', 'Phone Numbers']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            name = extract_name(url, soup)

            if name != 'N/A':
                emails, phones = extract_contacts(soup, response.text)
                email = match_email_to_name(name, emails) if emails else ''

                writer.writerow({
                    'Name': name,
                    'URL': url,
                    'Emails': email,
                    'Phone Numbers': ', '.join(phones)
                })

                print(f"Extracted details for {name}")
            else:
                print(f"Skipped irrelevant name from {url}")

        except Exception as e:
            print(f"Failed to extract from {url}: {e}")

print(f"Researcher details saved to {output_csv}")
