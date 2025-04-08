from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import tempfile
import os
import logging
import traceback
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def fetch_bbc_news():
    URL = "https://www.bbc.com/news/business"
    response = requests.get(URL)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    headlines_data = []
    for h2_tag in soup.find_all("h2", class_=["sc-87075214-3", "eywmDE", "czAFqs", "hxmZpj"]):
        headline_text = h2_tag.get_text(strip=True)
        link_tag = h2_tag.find_parent("a")
        link = "https://www.bbc.com" + link_tag['href'] if link_tag and 'href' in link_tag.attrs else "#"
        headlines_data.append({
            "title": headline_text,
            "url": link,
            "source": "bbc",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return headlines_data

def fetch_les_echos_news():
    # Create Chrome options
    options = Options()
    options.headless = True  # Headless mode enabled
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")  # Path to Chrome binary
    
    if not options.binary_location:
        raise EnvironmentError("Chrome binary path not found. Please set 'GOOGLE_CHROME_BIN' environment variable.")
    
    # Chrome options to prevent any Chrome-specific issues
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    
    # Specify the path to ChromeDriver using Service
    service = Service(ChromeDriverManager().install())
    
    # Create a unique user data directory for each session
    user_data_dir = tempfile.mkdtemp()  # This creates a unique temporary directory
    options.add_argument(f"--user-data-dir={user_data_dir}")
    
    # Initialize WebDriver with the service and options
     try:
        # Initialize WebDriver with options and service
        driver = webdriver.Chrome(service=service, options=options)
        
        # Open the URL
        driver.get("https://www.lesechos.fr/finance-marches")
        
        # Initialize list to store news data
        news = []
        
        # Find all headline elements on the page
        headlines = driver.find_elements(By.TAG_NAME, "h3")
        
        # Loop through all the headlines
        for headline in headlines:
            title = headline.text.strip()  # Get the title of the headline
            
            try:
                # Try to find the parent link for each headline
                parent_link = headline.find_element(By.XPATH, "..").get_attribute("href")
                
                # If the link is valid and matches the domain, append the news data
                if parent_link and parent_link.startswith("https://www.lesechos.fr"):
                    news.append({
                        "title": title,
                        "url": parent_link,
                        "source": "lesechos",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            except Exception as e:
                # Handle any errors with a message
                print(f"An error occurred while processing the headline: {e}")
                continue  # Skip this headline and continue with the next one
        
        # Quit the driver after processing
        driver.quit()

        # Return the scraped news
        return news

    except Exception as e:
        # If WebDriver initialization or page load fails
        print(f"An error occurred while initializing the WebDriver: {e}")
        
        if 'driver' in locals():  # Check if driver was created before quitting
            driver.quit()

        # Return empty list in case of failure
        return []

    

@app.route('/')
def home():
    try:
        print("Fetching news...")
        # Fetching data
        bbc_news = fetch_bbc_news()
        print(f"BBC News fetched: {len(bbc_news)} articles")
        les_echos_news = fetch_les_echos_news()
        print(f"Les Echos News fetched: {len(les_echos_news)} articles")
        
        all_news = bbc_news + les_echos_news
        # Sort by timestamp descending
        all_news.sort(key=lambda x: x["timestamp"], reverse=True)
        
        print(f"Total news articles: {len(all_news)}")

        return render_template('index.html', all_news=all_news)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        logging.error(traceback.format_exc())
        return "An error occurred while fetching the news", 500

if __name__ == "__main__":
    app.run(debug=True)
