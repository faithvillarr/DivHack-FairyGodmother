# randomly select a pin from a given board to extract the color palette
# install selenium, beautiful soup (python3-bs4), webdriver-manager, Pillow
# NOTE: currently returns nothing but opens chosen image on local device

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
from PIL import Image
import io
import random

# Function to download image from URL
def collect_image(image_url, save_folder="downloads"):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    return requests.get(image_url).content # image byte stream

# Function to get the image URL from a Pinterest pin
def get_pin_image_url(pin_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(pin_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find image URL (Pinterest images are often stored in <img> tags with 'src' or 'srcset' attributes)
    img_tag = soup.find("img", {"src": True})
    
    if img_tag:
        return img_tag["src"]
    else:
        print(f"Image not found in pin: {pin_url}")
        return None

# Function to scroll and extract pin URLs from the dynamically loaded Pinterest page
def get_pins_from_board_with_scroll(board_url, max_pins=50):
    # Set up Chrome options (you can also use a headless browser by uncommenting the option below)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")  # Uncomment if you want to run in headless mode

    # Provide path to your ChromeDriver
    driver_service = Service()  # Update with the actual path to your chromedriver
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    # Open the Pinterest board URL
    driver.get(board_url)
    
    pin_urls = set()
    scroll_pause_time = 2  # Adjust the pause time between scrolls if needed
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # Keep scrolling until we collect enough pins or reach the bottom
    while len(pin_urls) < max_pins:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # Wait for the page to load more content

        # Extract pin URLs from the loaded content
        pins = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/pin/"]')
        
        for pin in pins:
            href = pin.get_attribute("href")
            if href and "/pin/" in href:
                pin_urls.add(href)
        
        # Break if we have collected enough pins
        if len(pin_urls) >= max_pins:
            break
        
        # Calculate new scroll height and compare it with the last scroll height to check if we reached the bottom
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Reached the end of the page.")
            break
        last_height = new_height
    
    driver.quit()
    return list(pin_urls)[:max_pins]

# Main function to scrape and download pins from a board with Selenium
def collect_pins_from_board(board_url, max_pins=50, save_folder="downloads"):
    print(f"Scraping board: {board_url}")

    # Use Selenium to scroll and collect pin URLs
    pin_urls = get_pins_from_board_with_scroll(board_url, max_pins)
    
    if not pin_urls:
        print("No pins found.")
        return
    
    print(f"Found {len(pin_urls)} pins. Collecting images...")
    images = []

    # Download the images for all collected pins
    for pin_url in pin_urls:
        image_url = get_pin_image_url(pin_url)
        if image_url:
            images.append(collect_image(image_url, save_folder))

    return random.choice(images), len(pin_urls)


# Example usage
def choose_pin(board_url):
    try:
        image, num_pins_obtained = collect_pins_from_board(board_url, max_pins=MAX_PINS)

        if num_pins_obtained < MAX_PINS:
            choose_pin(board_url)
        
        return Image.open(io.BytesIO(image))
    except:
        print("Initial run failed to download " + str(MAX_PINS) + " pins. Trying again...")
        choose_pin(board_url)

if __name__ == "__main__":
    board_url = "https://www.pinterest.com/bookeater999/fall-2024/"  # Replace with actual Pinterest board URL
    MAX_PINS = 20  # Set the maximum number of pins you want to download
    CHROMEDRIVER_PATH = "C:\Program Files\Google\Chrome"

    print(type(choose_pin(board_url)))
    print(type(Image))