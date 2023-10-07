from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
# Configure Chrome Options
chrome_options = Options()
chrome_options.headless = True  # Run in headless mode

# Initialize the Chrome driver
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
# Open the landing page
url = "https://www.acu.edu.au/study-at-acu/fees-and-scholarships/other-fees-and-costs"
driver.get(url)

# Use BeautifulSoup to parse the page and extract all links
soup = BeautifulSoup(driver.page_source, 'html.parser')
all_links = [a['href'] for a in soup.find_all('a', href=True)]

# This will hold all the extracted text
all_texts = []
# exclude_pattern = r'^(cookie|privacy|#|policy)'
# filtered_links = [link for link in all_links if not re.match(exclude_pattern,link)]
# Define keywords to filter
keywords = ['privacy', 'cookie', 'policy', '#']

# Create a new list with filtered links
filtered_links = [link for link in all_links if all(keyword not in link for keyword in keywords)]

print(filtered_links)
for link in filtered_links:
    try:
        driver.get(link)
        page_text = driver.find_element(By.TAG_NAME, 'body').text
        all_texts.append(page_text)
    except Exception as e:
        print(f"Error accessing {link}: {e}")

driver.quit()

# Now, all_texts contains texts from each link you navigated to

# Save the extracted text to a text file
text_output_path = "./extracted_text.txt"
with open(text_output_path, 'w', encoding='utf-8') as text_file:
    for text in all_texts:
        text_file.write(text + '\n')

print(f"Text has been saved to: {text_output_path}")
