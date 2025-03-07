from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random

def scrape_bestbuy_selenium(url):
    try:
        # Set up Chrome options (optional)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')  # Add a user agent

        # Set the path to the ChromeDriver executable
        webdriver_service = Service("C:\ALL IN ONE\DYNAMIC PRICING\selenium\chromedriver.exe")  # Replace with the actual path

        # Create a new Chrome driver instance
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

        # Load the URL
        driver.get(url)

        # Wait for the page to load (adjust the sleep time as needed)
        time.sleep(random.uniform(3, 5))

        # Get the HTML source code
        html = driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        products = []
        product_elements = soup.find_all('li', class_='sku-item')  # Adjust the class name as needed

        for product_element in product_elements:
            try:
                name_element = product_element.find('a', class_='sku-title')
                name = name_element.text.strip() if name_element else "N/A"

                price_element = product_element.find('div', class_='priceView-customer-price')
                price_span = price_element.find('span', {'aria-hidden': 'true'})
                price = price_span.find_next_sibling("span").text if price_element else "N/A"

                products.append({'name': name, 'price': price})
            except Exception as e:
                print(f"Error extracting data for a product: {e}")

        return products

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        try:
            driver.quit()  # Close the browser window
        except:
            pass

if __name__ == '__main__':
    url = 'https://www.bestbuy.com/site/laptops/all-laptops/pcmcat138500050000.c?id=pcmcat138500050000'  # Replace with the URL of the page you want to scrape
    products = scrape_bestbuy_selenium(url)

    if products:
        for product in products:
            print(f"Name: {product['name']}, Price: {product['price']}")
    else:
        print("Could not retrieve product data.")