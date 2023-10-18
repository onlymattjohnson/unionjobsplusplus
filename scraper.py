import re, requests, sqlite3
from bs4 import BeautifulSoup
from datetime import date


def create_connection(db_file):
    """
    Creates a connection to the SQLite file
    :param db_file: The database file
    :return: A connection object or None
    """

    con = None
    try:
        con = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return con

def load_employer(con, employer_name):
    """
    Loads an employer to the database
    :param con:
    :param employer_name:
    :return: employer id
    """

    sql = ''' INSERT INTO employer(employer_name)
              VALUES (?)'''

    cur = con.cursor()
    cur.execute(sql, employer_name)
    con.commit()

    return cur.lastrowid

if __name__ == '__main__':
    con = create_connection('unionjobs.db')

    url = 'https://www.unionjobs.com/staffing_list.php'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html5lib')

    employers = soup.find_all('div', {'class': 'employer'})

    for org in employers:
        employer_name = org.find_all('h3')[0].text.strip()
        # remove multiple spaces from org names
        # this converts something like UNITE HERE (Local                 1) to UNITE HERE (Local 1)
        employer_name = re.sub(' +', ' ', employer_name)
        with con:
            load_employer(con, employer_name)
        
        jobs = org.find_all('li')
        for job in jobs:
            job_text = job.text.strip()

            job_link = job.find('a')['href']
            
            # Extract Union Jobs ID
            job_id_search = re.search('id=(.*)', job_link)
            job_id = int(job_id_search.group(1))
            
            job_link = f'https://www.unionjobs.com{job_link}'
            
            job_title = job.find('a').text.strip()
            
            job_posted_string = re.search('\(Posted: (\d{1,20})\/(\d{1,2})\/(\d{4})\)', job_text)
            job_posted_string_day = int(job_posted_string.group(1))
            job_posted_string_month = int(job_posted_string.group(2))
            job_posted_string_year = int(job_posted_string.group(3))
            job_posted_date = date(job_posted_string_year, job_posted_string_day, job_posted_string_day)
            
            job_location = re.search('\(Posted: .*\)(.+)', job_text).group(1).strip()
            # print(f'{job_title} with {employer_name} in {job_location} on {job_posted_date}')