import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_jobs(last_page):
    jobs = []
    for i in range(last_page):
        print(f"Scrapping Indeed: Page {i+1}")
        result = requests.get(f"{URL}&start={i * LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            title = result.find("h2").find("a")["title"]
            company = result.find("span", {"class": "company"})
            if company:
                company_link = company.find("a")
                if company_link is None:
                    company = str(company.string).strip()
                else:
                    company = str(company_link.string).strip()
            else:
                company = None

            location = result.find("div", {"class": "recJobLoc"})["data-rc-loc"]
            apply_link = f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={result['data-jk']}"

            jobs.append({"title": title, "company": company, "location": location, "apply_link": apply_link})
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs