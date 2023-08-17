from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fpdf import FPDF

# Configure Chrome Options
chrome_options = Options()
chrome_options.headless = True  # Run in headless mode

# Initialize the Chrome driver
service = Service('/Users/ankitbhandari/Scrappy/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the landing page
url = "https://www.acu.edu.au/study-at-acu/fees-and-scholarships/other-fees-and-costs"
driver.get(url)

# Use BeautifulSoup to parse the page and extract all links
soup = BeautifulSoup(driver.page_source, 'html.parser')
links = [a['href'] for a in soup.find_all('a', href=True)]

# This will hold all the extracted text
all_texts = []

for link in links:
    try:
        driver.get(link)
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        all_texts.append(page_text)
    except Exception as e:
        print(f"Error accessing {link}: {e}")

driver.quit()

# Now, all_texts contains texts from each link you navigated to
# Create a new PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

# Add each extracted text to the PDF
max_chars = 500  # Example value; adjust as needed
for text in all_texts:
    text = text.encode('latin-1', 'replace').decode('latin-1')
    for text_chunk in [text[i:i+max_chars] for i in range(0, len(text), max_chars)]:
        pdf.multi_cell(0, 10, txt=text_chunk, border=0, align='L')

# Save the PDF to a file
pdf_output_path = "/Users/ankitbhandari/Scrappy/extracted_text.pdf"
pdf.output(pdf_output_path)

print(f"Text has been saved to: {pdf_output_path}")
