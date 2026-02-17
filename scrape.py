import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import os

# The exact names to look for in the table
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
    try:
        response = requests.get(url, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'border': '1'})
        
        new_data = []
        today = datetime.date.today().strftime("%Y-%m-%d")

        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) >= 11:
                name = cols[0].text.strip()
                # Fuzzy match: check if our target keyword is in the table row name
                if any(target.lower() in name.lower() for target in target_products):
                    new_data.append({
                        "Date": today,
                        "Commodity": name,
                        "Current_Price": cols[2].text.strip(),
                        "One_Week_Back": cols[8].text.strip(),
                        "One_Month_Back": cols[9].text.strip(),
                        "One_Year_Back": cols[10].text.strip()
                    })

        df_new = pd.DataFrame(new_data)
        file_path = "data/prices.csv"

        # Append to existing file if it exists, otherwise create it
        if os.path.exists(file_path):
            df_new.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df_new.to_csv(file_path, index=False)
        
        print(f"Successfully added {len(new_data)} rows for {today}")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    scrape()
