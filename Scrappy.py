from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fpdf import FPDF
from urllib.parse import urlparse, urljoin

# Configure Chrome Options
chrome_options = Options()
chrome_options.headless = True  # Run in headless mode

# Initialize the Chrome driver
# You need to assign the path on the basis of your local machine
service = Service('/Users/ankitbhandari/Scrappy/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the landing page
url = input("Enter URL- ")
parsed_input_url = urlparse(url)
domain = parsed_input_url.netloc
print(f"Accessing: {url}")
driver.get(url)

# Use BeautifulSoup to parse the page and extract all links
soup = BeautifulSoup(driver.page_source, 'html.parser')
all_links = [a['href'] for a in soup.find_all('a', href=True)]

# Correct relative links and filter for same domain links
links = []
for link in all_links:
    absolute_link = urljoin(url, link)
    if urlparse(absolute_link).netloc == domain:
        links.append(absolute_link)

all_texts = []

for link in links:
    try:
        print(f"Accessing: {link}")
        driver.get(link)
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        all_texts.append(page_text)
    except Exception as e:
        print(f"Failed to access: {link}. Error: {e}")

driver.quit()

for text in all_texts:
    print(text)

# Create a new PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 12)

# Add each extracted text to the PDF
for text in all_texts:
    text = text.encode('utf-8').decode('latin-1', 'replace')
    pdf.multi_cell(0, 10, txt=text, border=0, align='L')

# Save the PDF to a file
pdf_output_path = "/Users/ankitbhandari/Scrappy/extracted_text.pdf"
pdf.output(pdf_output_path)

print(f"Text has been saved to: {pdf_output_path}")
