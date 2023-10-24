import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv('full_data.csv')






def scrape_data(row):
    try:
        
        url = row['link']
        print(url)

        if row['scraped'] == True:
            print('Already Scraped, Skipping')
            return
        
        driver = webdriver.Chrome(service=ChromeService())
        driver.get(url)
        driver.implicitly_wait(10)

        title = driver.find_element(By.CLASS_NAME, 'product-header__title').text
        tagline = driver.find_element(By.CLASS_NAME, 'product-header__tagline').text
        revenue = driver.find_element(By.CLASS_NAME, 'product-metrics__stat--revenue').text
        site_link = driver.find_element(By.CSS_SELECTOR, '.product-header__title a').get_attribute('href')
       
        try:
            about = driver.find_element(By.CLASS_NAME, 'product-sidebar__description').text
            about = about.replace("ABOUT","")
        except: 
            about = "No data"


        try:
            twitter = driver.find_element(By.CLASS_NAME, 'product-metrics__stat--twitter').get_attribute('href')
        except: 
            twitter = "No Data"




        try:
            visitors = driver.find_element(By.CLASS_NAME, 'product-metrics__stat--visitors').text
            visitors = visitors.replace("VISITORS","").replace("\n","")
        except: 
            visitors = "No Data"
            
        try:
            founder_elements = driver.find_elements(By.CSS_SELECTOR, '.product-sidebar__users .user-link__name')
            founders = [founder_element.text for founder_element in founder_elements]
        except:
            founders = "No Data"

        tags_elements = driver.find_elements(By.CLASS_NAME, 'tag-list__tag')
        tags = [tag_element.text for tag_element in tags_elements]

        founder_link_elements = driver.find_elements(By.CLASS_NAME, 'user-link__link')
        founder_links = {founder_link_element.get_attribute('href') for founder_link_element in founder_link_elements}

        target_rows = df[df["link"] == url]

        # Check if any rows were found
        if not target_rows.empty:
            # Assuming you want to fill a column named 'AdditionalData' with value 'SomeValue'
            df.loc[df["link"] == url, 'title'] = title
            df.loc[df["link"] == url, 'tagline'] = tagline
            df.loc[df["link"] == url, 'revenue_inner_page'] = revenue.replace("\n","").replace("REVENUE","")
            df.loc[df["link"] == url, 'site_link'] = site_link
            df.loc[df["link"] == url, 'tags'] = str(tags)
            df.loc[df["link"] == url, 'founder_links'] = str(founder_links)
            df.loc[df["link"] == url, 'about'] = about
            df.loc[df["link"] == url, 'scraped'] = "TRUE"
            df.loc[df["link"] == url, 'twitter'] = twitter
            df.loc[df["link"] == url, 'visitors'] = visitors
            df.loc[df["link"] == url, 'founders'] = str(founders)
            
            
        else:
            print(f"No rows found for URL: {url}")
        
        print(df[df["link"] == url])

        # Specify the file path along with the file name and extension (e.g., 'data.csv')
        file_path = 'full_data.csv'

        # Save the dataframe to a CSV file
        df.to_csv(file_path, index=False)
        print("---------------------------------------------------------------")

        time.sleep(10)
        driver.quit()


    except:
        print("Skipping this , faced exception")
        driver.quit()


rows_to_process = df.iterrows()
executor = ThreadPoolExecutor(max_workers=10)
futures = [executor.submit(scrape_data, row) for _, row in rows_to_process]
executor.shutdown()
