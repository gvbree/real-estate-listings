from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import requests
import pandas as pd
import time
import re
import math

def api_client(
        driver, 
        real_estate_search_type:str,
        load_type:str = "preview",
        base_url:str = config.LISTINGS_PLATFORM_URL,
        wait_time:int = 5,
        n_objects_per_page:int = 200,
        n_pages_per_session:int = 50
    ):

    def get_fresh_session_details():
        real_estate_types_mapping = {
            "sale_apartment": "Wohnung kaufen", "sale_house": "Haus kaufen",
            "rent_apartment": "Wohnung mieten", "rent_house": "Haus mieten"
        }
        real_estate_search_term = real_estate_types_mapping[real_estate_search_type]

        driver.get(base_url)
        print(f"Browser opened, navigating to {base_url}")
        wait = WebDriverWait(driver, 15)
        time.sleep(wait_time)
        del driver.requests
        
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))).click()
            print("Cookies accepted")
        except:
            print("No cookie dialog")
            
        # Selecting search term in dropdown
        dropdown = Select(driver.find_element(By.ID, "searchid-select"))
        dropdown.select_by_visible_text(real_estate_search_term)

        # Get number of pages to scrape based on load type
        if load_type == "full":
            time.sleep(wait_time)
            search_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="search-submit-button"]')
            search_button_text = search_button.text
            n_objects = int(re.sub(r"\D", "", search_button_text))
            n_pages = math.ceil(n_objects / n_objects_per_page)
            print(f"Found {n_objects} objects. {n_pages} pages need to be scanned for a full load.")
        elif load_type == "preview":
            n_pages = 3
            print(f"Only scanning a preview of the data -> {n_pages} pages.")

        # Click search button according to search term
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-submit-button']"))).click()
        print(f"Clicking search for search term '{real_estate_search_term}'")
        
        # Start session including cookies and headers
        time.sleep(wait_time)
        cookies = {c["name"]: c["value"] for c in driver.get_cookies()}
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Referer": config.LISTINGS_PLATFORM_URL,
            "x-wh-client": config.X_WH_CLIENT
        })
        session.cookies.update(cookies)
        
        # Capture the base API URL to be used for scraping data via API calls
        captured_url = None
        for req in driver.requests:
            print(f"URL: {req.url} | Status: {req.response.status_code if req.response else 'No Response'}")
            if req.response and config.API_SEARCH_PATTERN in req.url and "sfId=" in req.url:
                captured_url = req.url.replace("page=1&", "")
                print("Base API URL captured: ", captured_url)
        if not captured_url:
            print("Base API URL not found")
        
        return session, captured_url, n_pages
    
    all_rows = []
    session, base_api_url, n_pages = get_fresh_session_details()
                
    for page in range(1, n_pages + 1):    
        if page > 1 and (page - 1) % n_pages_per_session == 0:
            print(f"\n--- Refreshing Session at Page {page} to avoid 504 Gateway Timeout errors ---")
            session, base_api_url, n_pages = get_fresh_session_details()
    
        params = {"page": page, "rows": n_objects_per_page}
        r = session.get(base_api_url, params=params)
        r.raise_for_status() 
        data = r.json()
        
        for advert in data["advertSummaryList"]["advertSummary"]:
            row = {item.get("name"): item.get("values")[0] 
                   for item in advert.get("attributes", {}).get("attribute", [])}
            all_rows.append(row)
                
        rowsReturned = data.get("rowsReturned", "")
        print(f"GET {r.url} -> {rowsReturned} results")
    
    driver.quit()
    print("Browser closed")
    
    df = pd.DataFrame(all_rows)
    print(f"\nTotal listings scraped: {len(df)}")
    
    return df