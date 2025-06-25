from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

app = Flask(__name__)

def fetch_bbc_news():
    URL = "https://www.bbc.com/news/business"
    response = requests.get(URL)

    if response.status_code != 200:
        print(f"Failed to fetch BBC. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    headlines_data = []
    for h2_tag in soup.find_all("h2", class_=["sc-87075214-3", "eywmDE", "czAFqs", "hxmZpj"]):
        headline_text = h2_tag.get_text(strip=True)
        link_tag = h2_tag.find_parent("a")
        
        if link_tag and 'href' in link_tag.attrs:
            link = "https://www.bbc.com" + link_tag['href']
        else:
            link = "#"
        
        headlines_data.append({
            "title": headline_text,
            "url": link,
            "source": "bbc",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return headlines_data

#def fetch_les_echos_news():
    #options = webdriver.ChromeOptions()
    #options.add_argument("user-agent=Mozilla/5.0")
    #options.add_argument("--disable-blink-features=AutomationControlled")
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")

    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #driver.get("https://www.lesechos.fr/finance-marches")

    #news = []
    #headlines = driver.find_elements(By.TAG_NAME, "h3")

    #for headline in headlines:
        #title = headline.text.strip()
        #try:
            #parent_link = headline.find_element(By.XPATH, "..").get_attribute("href")
            #if parent_link and parent_link.startswith("https://www.lesechos.fr"):
                #news.append({
                    #"title": title,
                    #"url": parent_link,
                    #"source": "lesechos",
                    #"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #})
        #except Exception as e:
            #print(f"Error while fetching link for headline: {title}, error: {e}")

    #driver.quit()
    #return news

@app.route('/')
def home():
    bbc_news = fetch_bbc_news()
    #les_echos_news = fetch_les_echos_news()
    all_news = bbc_news
    # Sort by timestamp descending
    all_news.sort(key=lambda x: x["timestamp"], reverse=True)
    return render_template('index.html', all_news=all_news)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

