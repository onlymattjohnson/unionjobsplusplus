import re, requests, sqlite3
from bs4 import BeautifulSoup
from datetime import date

url = 'https://www.unionjobs.com/staffing_list.php'
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html5lib')

organizations = soup.find_all('div', {'class': 'organization'})

for org in organizations:
    organization_name = org.find_all('h3')[0].text.strip()
    # remove multiple spaces from org names
    # this converts something like UNITE HERE (Local                 1) to UNITE HERE (Local 1)
    organization_name = re.sub(' +', ' ', organization_name)
    jobs = org.find_all('li')
    for job in jobs:
        job_text = job.text.strip()

        job_link = job.find('a')['href']
        job_link = f'https://www.unionjobs.com{job_link}'
        
        job_title = job.find('a').text.strip()
        
        job_posted_string = re.search('\(Posted: (\d{1,20})\/(\d{1,2})\/(\d{4})\)', job_text)
        job_posted_string_day = int(job_posted_string.group(1))
        job_posted_string_month = int(job_posted_string.group(2))
        job_posted_string_year = int(job_posted_string.group(3))
        job_posted_date = date(job_posted_string_year, job_posted_string_day, job_posted_string_day)
        
        job_location = re.search('\(Posted: .*\)(.+)', job_text).group(1).strip()
        print(f'{job_title} with {organization_name} in {job_location} on {job_posted_date}')