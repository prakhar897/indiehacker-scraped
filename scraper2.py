import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from concurrent.futures import ThreadPoolExecutor
import re
import requests

df = pd.read_csv('full_data.csv')

def scrape_data(row):
    try:
        
        url = row['site_link']
        print(url)

        if (row['scraped2'] == True) or (url == "https://womp.xyz/"):
            print('Already Scraped, Skipping')
            return
        
        driver = webdriver.Chrome(service=ChromeService())
        driver.implicitly_wait(10)
        driver.get(url)

        target_rows = df[df["site_link"] == url]

        page_source = driver.page_source
        grabbedEmails = set(re.findall(r'[a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+', page_source))
        grabbedEmails = {item for item in grabbedEmails if not item.endswith(('.png', '.webp', '.jpg', '.jpeg', '.mp4'))}

        print(str(list(grabbedEmails)))

        # Check if any rows were found
        if not target_rows.empty:
            # Assuming you want to fill a column named 'AdditionalData' with value 'SomeValue'
            df.loc[df["site_link"] == url, 'grabbedEmails'] = str(list(grabbedEmails))
            df.loc[df["site_link"] == url, 'scraped2'] = "TRUE"
            
            
            
        else:
            print(f"No rows found for URL: {url}")
        
        print(df[df["site_link"] == url])

        # Specify the file path along with the file name and extension (e.g., 'data.csv')
        file_path = 'full_data.csv'

        # Save the dataframe to a CSV file
        df.to_csv(file_path, index=False)
        print("---------------------------------------------------------------")

        driver.quit()

    


    except:
        print("Skipping this , faced exception")
        driver.quit()


rows_to_process = df.iloc[380:].iterrows()
# rows_to_process = df.iterrows()
executor = ThreadPoolExecutor(max_workers=10)
futures = [executor.submit(scrape_data, row) for _, row in rows_to_process]
executor.shutdown()

# for _, row in df.iterrows():
#     scrape_data(row)
#     #break
