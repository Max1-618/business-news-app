import logging
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    try:
        # Fetching data
        bbc_news = fetch_bbc_news()
        les_echos_news = fetch_les_echos_news()
        all_news = bbc_news + les_echos_news
        # Sort by timestamp descending
        all_news.sort(key=lambda x: x["timestamp"], reverse=True)

        return render_template('index.html', all_news=all_news)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        logging.error(traceback.format_exc())
        return "An error occurred while fetching the news", 500

# Your fetch_bbc_news and fetch_les_echos_news functions remain the same

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
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    driver.get("https://www.lesechos.fr/finance-marches")
    news = []
    headlines = driver.find_elements(By.TAG_NAME, "h3")
    for headline in headlines:
        title = headline.text.strip()
        try:
            parent_link = headline.find_element(By.XPATH, "..").get_attribute("href")
            if parent_link and parent_link.startswith("https://www.lesechos.fr"):
                news.append({
                    "title": title,
                    "url": parent_link,
                    "source": "lesechos",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        except:
            continue
    driver.quit()
    return news

@app.route('/', methods=["GET", "HEAD"])
def home():
    bbc_news = fetch_bbc_news()
    les_echos_news = fetch_les_echos_news()
    all_news = bbc_news + les_echos_news
    all_news.sort(key=lambda x: x["timestamp"], reverse=True)
    return render_template('index.html', all_news=all_news)

if __name__ == "__main__":
    app.run(debug=True)
