import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_jobs_from_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    try:
        page = requests.get(url, headers=headers)
        page.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching page {url}: {e}")
        return []

    soup = BeautifulSoup(page.text, 'html.parser')
    job_elements = soup.find_all('div', class_='jobsearch-SerpJobCard')  # Fixed class name
    jobs = []

    for job_element in job_elements:  # Fixed variable name
        try:
            title = job_element.find('h2', class_='title').a.text.strip()  # Fixed class name
            company = job_element.find('span', class_='company').text.strip()  # Fixed class name
            location = job_element.find('div', class_='location').text.strip() if job_element.find('div', class_='location') else "N/A"  # Fixed class name
            summary = job_element.find('div', class_='summary').text.strip()  # Fixed class name

            job = {
                'Title': title,
                'Company': company,
                'Location': location,
                'Summary': summary
            }
            jobs.append(job)
        except AttributeError as e:
            logging.warning(f"Error parsing job data: {e}")
            continue

    return jobs

if __name__ == "__main__":  # Corrected main block
    base_url = 'https://www.indeed.com/jobs?q=software+developer&start='
    all_jobs = []
    for page in range(0, 50, 10):  # Scrape the first 5 pages (10 jobs per page)
        logging.info(f'Scraping page: {page // 10 + 1}')
        url = base_url + str(page)
        jobs = get_jobs_from_page(url)
        if not jobs:
            break
        all_jobs.extend(jobs)

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        df.to_csv('Jobs.csv', index=False)
        df.to_excel('Jobs.xlsx', index=False)
        logging.info('Scraping complete. Data saved to Jobs.csv and Jobs.xlsx.')
    else:
        logging.info('No data scraped.')
