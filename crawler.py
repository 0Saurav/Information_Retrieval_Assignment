# Polite crawling version with authors + year + type (fixed)

import json
import os
import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Base URL
BASE_URL = "https://pureportal.coventry.ac.uk/en/organisations/fbl-school-of-economics-finance-and-accounting/publications/"

# Crawl delay from robots.txt
CRAWL_DELAY = 5  # seconds


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # uncomment for no browser window
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def fetch_publications(driver, base_url):
    all_publications = []
    page_number = 0

    driver.get(base_url)
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler'))
        )
        print("[info] Accepting cookies...")
        driver.execute_script("arguments[0].click();", cookie_button)
        time.sleep(1)
    except TimeoutException:
        print("[info] No cookie popup found.")

    while True:
        current_url = f"{base_url}?page={page_number}"

        # Skip disallowed URLs
        if "?format=rss" in current_url or "?export=xls" in current_url:
            print(f"[skip] Disallowed by robots.txt: {current_url}")
            page_number += 1
            continue

        print(f"\n--- Scraping Page {page_number+1}: {current_url} ---")
        driver.get(current_url)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "result-container"))
            )
        except TimeoutException:
            print("[done] No results found, stopping.")
            break

        publication_divs = driver.find_elements(By.CLASS_NAME, "result-container")
        if not publication_divs:
            print("[done] Empty page, finished crawling.")
            break

        for pub_div in publication_divs:
            try:
                # Title + link
                title_tag = pub_div.find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a")
                title = title_tag.text.strip()
                link = title_tag.get_attribute("href")

                # Authors (try both selectors)
                try:
                    author_tags = pub_div.find_elements(By.CSS_SELECTOR, "span.person")
                    if not author_tags:
                        author_tags = pub_div.find_elements(By.CSS_SELECTOR, "a.link.person")
                    authors = ", ".join([a.text.strip() for a in author_tags if a.text.strip()])
                    if not authors:
                        authors = "N/A"
                except:
                    authors = "N/A"

                # Year
                try:
                    year_tag = pub_div.find_element(By.CSS_SELECTOR, "span.date")
                    year = year_tag.text.strip()
                except:
                    year = "N/A"

                # Type / Venue
                try:
                    type_tag = pub_div.find_element(By.CSS_SELECTOR, "span.type")
                    pub_type = type_tag.text.strip()
                except:
                    pub_type = "N/A"

                all_publications.append({
                    "title": title,
                    "link": link,
                    "authors": authors,
                    "year": year,
                    "type": pub_type
                })
            except Exception as e:
                print(f"[warn] Skipped one publication: {e}")
                continue

        print(f"[info] Collected {len(publication_divs)} publications from this page.")

        page_number += 1

        # Polite crawl: wait at least CRAWL_DELAY seconds + random small extra
        sleep_time = CRAWL_DELAY + random.uniform(0, 2)
        print(f"[info] Sleeping for {sleep_time:.2f} seconds to respect robots.txt...")
        time.sleep(sleep_time)

    return all_publications


def save_results(publications, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save JSON
    json_path = os.path.join(folder_path, "publications.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(publications, f, indent=4, ensure_ascii=False)
    print(f"[done] Saved JSON: {json_path}")

    # Save CSV
    csv_path = os.path.join(folder_path, "publications.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link", "authors", "year", "type"])
        writer.writeheader()
        for pub in publications:
            writer.writerow(pub)
    print(f"[done] Saved CSV: {csv_path}")


def main():
    driver = setup_driver()
    try:
        publications = fetch_publications(driver, BASE_URL)
        # remove duplicates
        unique_publications = [dict(t) for t in {tuple(d.items()) for d in publications}]
        print(f"\n✅ Total unique publications scraped: {len(unique_publications)}")

        save_results(unique_publications, r"E:\Information_Retrieval_Assignment\data")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
