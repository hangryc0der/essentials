import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import os

# Target products from your list
target_products = [
    "Rice", "Wheat", "Atta (Wheat)", "Gram Dal", "Tur/Arhar Dal", "Urad Dal", 
    "Moong Dal", "Masoor Dal", "Sugar", "Milk", "Groundnut Oil", "Soya Oil", 
    "Sunflower Oil", "Gur", "Tea Loose", "Salt", "Potato", "Onion", "Tomato", 
    "Ragi (whole)", "Suji (whole)", "Besan", "Desi Ghee", "Eggs", 
    "Black Pepper (whole)", "Coriander (whole)", "Cummin Seed (whole)", 
    "Red Chillies (whole)", "Turmeric (powder)", "Banana", "Ginger", "Garlic"
]

def scrape():
    url = "https://fcainfoweb.nic.in/Reports/DB/Dailyprices.aspx"
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Ensure data folder exists
    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'border': '1'})
        
        if not table:
            print("Could not find table on page.")
            return

        extracted_data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 11:
                name = cols[0].get_text(strip=True)
                # Fuzzy match to catch variations like "Milk (1Ltr)"
                if any(target.lower() in name.lower() for target in target_products):
                    extracted_data.append({
                        "Commodity": name,
                        "Current_Price": cols[2].get_text(strip=True),
                        "One_Week_Back": cols[8].get_text(strip=True),
                        "One_Month_Back": cols[9].get_text(strip=True),
                        "One_Year_Back": cols[10].get_text(strip=True)
                    })

        # Save to a NEW file for today
        df = pd.DataFrame(extracted_data)
        filename = f"data/prices_{today}.csv"
        df.to_csv(filename, index=False)
        print(f"File created: {filename} with {len(extracted_data)} items.")

    except Exception as e:
        print(f"Scraper failed: {e}")

if __name__ == "__main__":
    scrape()
