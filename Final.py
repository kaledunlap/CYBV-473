import requests
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag

# sets for unique data
unique_urls = set()
image_urls = set()
phone_numbers = set()
zip_codes = set()

# Text storage
all_text = ""

# Regex patterns from instruction sheet
zipPatt = re.compile(r'\b\d{5}(?:-\d{4})?\b')
phonePatt = re.compile(r'\(?\d{3}\)?-? *\d{3}-? *-?\d{4}')

def scrape_page(url):
    global all_text
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract and store URLs
    for link in soup.find_all('a', href=True):
        full_url = requests.compat.urljoin(url, link['href'])
        if "casl.website" in full_url:
            unique_urls.add(full_url)

    # Extract and store image URLs
    for img in soup.find_all('img', src=True):
        img_url = requests.compat.urljoin(url, img['src'])
        image_urls.add(img_url)

    # Extract and store phone numbers
    phone_numbers.update(phonePatt.findall(response.text))

    # Extract and store zip codes
    zip_codes.update(zipPatt.findall(response.text))

    # Extract and store text content
    all_text += soup.get_text(separator=' ', strip=True) + " "

# Starting page
start_url = "https://casl.website/"
scrape_page(start_url)

# Process text (NLTK)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

words = word_tokenize(all_text)
unique_vocab = set(w.lower() for w in words if w.isalpha())
verbs = {word for word, pos in pos_tag(words) if pos.startswith('VB')}
nouns = {word for word, pos in pos_tag(words) if pos.startswith('NN')}

# Generate report
report = f"""
Web Scraping Report:

1. Unique URLs Found:
{chr(10).join(sorted(unique_urls))}

2. Unique Image URLs Found:
{chr(10).join(sorted(image_urls))}

3. Phone Numbers Found:
{chr(10).join(sorted(phone_numbers))}

4. Zip Codes Found:
{chr(10).join(sorted(zip_codes))}

5. Unique Vocabulary:
{chr(10).join(sorted(unique_vocab))}

6. Verbs Found:
{chr(10).join(sorted(verbs))}

7. Nouns Found:
{chr(10).join(sorted(nouns))}

"""

# Save the report (using .txt file as export method and converting to PDF after)
with open("web_scrape_report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("Report generated successfully.")


'''
Sources used:

1. https://realpython.com/beautiful-soup-web-scraper-python/#step-2-scrape-html-content-from-a-page

2. https://realpython.com/flask-by-example-part-3-text-processing-with-requests-beautifulsoup-nltk/#display-results

3. https://dev.to/alexander_martin_13fd7a40/web-scraping-with-python-an-in-depth-guide-to-requests-beautifulsoup-selenium-and-scrapy-bm6#best-practices-for-web-scraping

'''
