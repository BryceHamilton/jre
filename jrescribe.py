from multiprocessing.pool import ThreadPool as Pool
import requests
from bs4 import BeautifulSoup

def scrape_jrescribe_pod(pod_num):
  URL = f"https://jrescribe.com/transcripts/p{pod_num}.html"
  page = requests.get(URL)

  soup = BeautifulSoup(page.content, "html.parser")

  p_tags = soup.find_all('p')
  doc_list = [p.get_text() for p in p_tags]
  doc =  ' '.join(doc_list)
  doc_no_footer = doc.split("Help improve this transcript!")[1]
  
  with open(f"transcripts/{pod_num}.txt", 'w') as f:
    f.write(doc_no_footer)

  title = soup.find('h1')
  splitter = "with " if "MMA" in title else " - "
  guest = title.split(splitter)[1]

  with open(f"guests/{pod_num}.txt", 'w') as f:
    f.write(guest)


def scrape_jrescribe():
  POD_START = 1104
  POD_END = 1266
  
  pool_size = 5
  pool = Pool(pool_size)

  for num in range(POD_START, POD_END):
    pool.apply_async(scrape_jrescribe_pod, (num,))

  pool.close()
  pool.join()
