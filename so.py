import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pages = soup.find("div", {"class", "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_jobs(last_page):
    jobs = []
    for i in range(last_page):
        result = requests.get(f"{URL}&pg={i+1}")
        print(f"Scrapping Stackoverflow : Page {i+1}")

        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            title = result.find("a", {"class": "s-link stretched-link"})["title"]
            company_location = result.find("h3", {"class": "fc-black-700"})
            company, location = company_location.find_all("span", recursive=False)
            company = company.get_text(strip=True).split("via")[0]
            location = location.get_text(strip=True)
            apply_link = f"https://stackoverflow.com/jobs/{result['data-jobid']}"
            jobs.append({"title": title, "company": company, "location": location, "apply_link": apply_link})
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
