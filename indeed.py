import requests
from bs4 import BeautifulSoup
#데이터 추출 beautifulsoup
LIMIT = 50
URL = f"https://jp.indeed.com/%E6%B1%82%E4%BA%BA?q=python&limit={LIMIT}"

#페이지의 마지막 번호를 가져옴.
def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    # pages = pages[:-1 ]
    # 마지막 한개는 지움
    max_page = pages[-1]
    return max_page

#각각의 채용정보 가져옴.
def extract_jobs(html):
    title = html.find("div", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    # results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://jp.indeed.com/viewjob?jk={job_id}"
    }

#각각의 페이지에서 채용정보(extract_jobs)를 가져오는 것.
def get_extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed: Page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extract_jobs(result)
        jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_pages()
  jobs = get_extract_jobs(last_page) 
  return jobs