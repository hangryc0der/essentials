import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import os

# Updated list to match official names in your document
target_products = [
    "Rice", "Wheat", "Atta (Wheat)", "Gram Dal", "Tur/Arhar Dal", "Urad Dal", 
    "Moong Dal", "Masoor Dal", "Sugar", "Milk", "Groundnut Oil", "Soya Oil", 
    "Sunflower Oil", "Gur", "Tea Loose", "Salt", "Potato", "Onion", "Tomato", 
    "Turmeric (powder)", "Banana", "Ginger"
]

def scrape():
    url = "https://fcainfoweb.nic.in/Reports/DB/Dailyprices.aspx"
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    if not os.path.exists('data'):
        os.makedirs('data')

    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        # The site uses a specific table structure
        table = soup.find('table', {'border': '1'})
        
        if not table:
            print("Website table not found.")
            return

        extracted_data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 11:
                name = cols[0].get_text(strip=True)
                # Check if product is in our target list
                if any(target.lower() in name.lower() for target in target_products):
                    extracted_data.append({
                        "Date": today,
                        "Commodity": name,
                        "Current_Price": cols[2].get_text(strip=True),
                        "1_Week_Back": cols[8].get_text(strip=True),
                        "1_Month_Back": cols[9].get_text(strip=True),
                        "1_Year_Back": cols[10].get_text(strip=True)
                    })

        if extracted_data:
            df = pd.DataFrame(extracted_data)
            filename = f"data/prices_{today}.csv"
            df.to_csv(filename, index=False)
            print(f"Success: Created {filename}")
        else:
            print("No matching products found today.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape()
