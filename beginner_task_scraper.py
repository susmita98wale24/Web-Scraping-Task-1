# -*- coding: utf-8 -*-
"""beginner_task_scraper.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1brNcDs3hRMBcGJuiM7kjQUKLr_tvXyz6
"""

# Install required libraries
!pip install requests beautifulsoup4 pandas

!pip install selenium pandas
!apt update
!apt install -y chromium-chromedriver

# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up Selenium options for Google Colab
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# URL of the e-commerce category page
url = 'https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops'

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Check if request was successful

# Parse the content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Open the URL
driver.get(url)
time.sleep(3)  # Wait for the page to load

# Lists to store the scraped data
product_names = []
prices = []
ratings = []

# Extract product containers
products = driver.find_elements(By.CLASS_NAME, 'thumbnail')

# Loop through each product and extract details
for product in products:
    # Extract product name
    name = product.find_element(By.CLASS_NAME, 'title').text
    product_names.append(name)

    # Extract price
    price = product.find_element(By.CLASS_NAME, 'price').text
    prices.append(price)

    # Extract rating (if available)
    rating_elements = product.find_elements(By.CLASS_NAME, 'ratings')
    rating = rating_elements[0].text if rating_elements else 'No Rating'
    ratings.append(rating)

# Close the browser
driver.quit()

# Check if data is extracted
if product_names:
    print("Data extracted successfully!")
else:
    print("No data found. Check the website structure or URL.")

# Create a DataFrame from the extracted data
data = pd.DataFrame({
    'Product Name': product_names,
    'Price': prices,
    'Rating': ratings
})

# Save the DataFrame to a CSV file
data.to_csv('products.csv', index=False)

# Display the DataFrame
data.head()

# Download the CSV file in Colab
from google.colab import files
files.download('products.csv')