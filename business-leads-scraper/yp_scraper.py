from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# فتح المتصفح
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://www.yellowpages.com/los-angeles-ca/restaurants"
driver.get(url)

time.sleep(5)  # استنى الصفحة تحمل

soup = BeautifulSoup(driver.page_source, "html.parser")

cards = soup.select("div.result")
data = []

for card in cards:
    name_tag = card.select_one("a.business-name")
    category_tags = card.select("div.categories a")
    phone_tag = card.select_one("div.phones")
    address_tag = card.select_one("div.street-address")
    locality_tag = card.select_one("div.locality")
    website_tag = card.select_one("a.track-visit-website")
    listing_tag = card.select_one("a.business-name")

    name = name_tag.get_text(strip=True) if name_tag else "N/A"
    category = ", ".join([c.get_text(strip=True) for c in category_tags]) if category_tags else "N/A"
    phone = phone_tag.get_text(strip=True) if phone_tag else "N/A"

    street = address_tag.get_text(strip=True) if address_tag else ""
    locality = locality_tag.get_text(strip=True) if locality_tag else ""
    address = f"{street}, {locality}".strip(", ") if (street or locality) else "N/A"

    website = website_tag.get("href") if website_tag and website_tag.get("href") else "N/A"

    if listing_tag and listing_tag.get("href"):
        href = listing_tag.get("href")
        listing_url = href if href.startswith("http") else "https://www.yellowpages.com" + href
    else:
        listing_url = "N/A"

    data.append({
        "Business Name": name,
        "Category": category,
        "Phone": phone,
        "Address": address,
        "Website": website,
        "Listing URL": listing_url
    })

driver.quit()

df = pd.DataFrame(data)

print(df.head())
print("Rows:", len(df))

df.to_excel("leads.xlsx", index=False)
print("Done ✅")