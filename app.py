from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
import os

def fetch_product_details(url):
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)

    driver.get(url)
    time.sleep(3)  

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    product_containers = soup.find_all("div", {"data-test": "product-item-name"})

    product_details_list = []

    for container in product_containers:
        title = container.get_text(strip=True)

        parent_container = container.find_parent()
        
        
        media_tag = parent_container.find(["img", "video"], {"class": "styles_thumbnail__Y9ZpZ"})
        if media_tag and media_tag.name == "img":
            media_src = media_tag['src']
        elif media_tag and media_tag.name == "video":
            media_src = media_tag.get('poster', 'Poster not found')
        else:
            media_src = "Media source not found"

        ratings_div = container.find_next("div", {"class": "ml-1 color-lighter-grey fontSize-12 fontWeight-400"})
        ratings = ratings_div.get_text(strip=True) if ratings_div else "Ratings not found"

        followers_div = container.find_next("div", {"class": "color-lighter-grey fontSize-12 fontWeight-400 styles_followersCount__Auv5S"})
        followers = followers_div.get_text(strip=True) if followers_div else "Followers not found"

        product_link_tag = container.find_parent("a", {"class": "color-darker-grey fontSize-16 fontWeight-400"})
        product_url = "https://www.producthunt.com" + product_link_tag['href'] if product_link_tag else "URL not found"

        product_details = {
            'Title': title,
            'Media Source URL': media_src,  
            'Ratings': ratings,
            'Followers': followers,
            'URL': product_url,
        }

        product_details_list.append(product_details)

    driver.quit()

    return product_details_list

product_category_url = "https://www.producthunt.com/topics/artificial-intelligence"

product_details_list = fetch_product_details(product_category_url)

def append_to_json_file(file_path, new_data):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
        existing_data.extend(new_data)
    else:
        existing_data = new_data

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

product_details_file_path = 'products.json'
append_to_json_file(product_details_file_path, product_details_list)

print(f"Product details have been appended to {product_details_file_path}")
