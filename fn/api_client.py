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
        n_objects_per_page:int = 200
    ):
    
    real_estate_types_mapping = {
        "sale_apartment": "Wohnung kaufen",
        "sale_house": "Haus kaufen",
        "rent_apartment": "Wohnung mieten",
        "rent_house": "Haus mieten"
    }

    real_estate_search_term = real_estate_types_mapping[real_estate_search_type]

    driver.get(base_url)
    print("Browser opened")
    
    wait = WebDriverWait(driver, 15)
    time.sleep(wait_time)
    
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))).click()
        print("Cookies accepted")
    except:
        print("No cookie dialog")
        
    dropdown = Select(driver.find_element(By.ID, "searchid-select"))
    dropdown.select_by_visible_text(real_estate_search_term)
    
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
        
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='search-submit-button']"))
    ).click()
    print(f"Selecting search: {real_estate_search_term}")
    
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
    
    all_rows = []
    
    for page in range(1, n_pages + 1):    
        if page == 1:
            base_api_url = None
            for req in driver.requests:
                if (
                    req.response
                    and config.API_SEARCH_PATTERN in req.url
                    and "sfId=" in req.url
                ):
                    base_api_url = req.url
                    base_api_url = base_api_url.replace("page=1&", "")
                    print("Base API URL captured: ", base_api_url)
            if not base_api_url:
                print("Base API URL not found")
                break
    
        params = {
            "page": page,
            "rows": n_objects_per_page,
        }
        
        r = session.get(base_api_url, params=params)
        r.raise_for_status()
        
        data = r.json()
        rows = []
        
        for advert in data["advertSummaryList"]["advertSummary"]:
            row = {}
            for key, value in advert.items():
                if key == "attributes":
                    attribute = advert[key]["attribute"]
                    for item in attribute:
                        name = item.get("name")
                        values = item.get("values")
                        row[name] = values[0]
            rows.append(row)
    
        all_rows.extend(rows)
        rowsReturned = data.get("rowsReturned", "")
        
        print(f"GET {r.url} -> {rowsReturned} results")
    
    driver.quit()
    print("Browser closed")
    
    df = pd.DataFrame(all_rows)
    print(f"\nTotal listings scraped: {len(df)}")
    
    return df