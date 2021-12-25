from multiprocessing.pool import ThreadPool as Pool
import requests
from bs4 import BeautifulSoup
from requests.api import get


def get_page_urls():
    base_url = "https://www.happyscribe.com/public/the-joe-rogan-experience"
    pages = []
    for page_num in range(1, 8):
        query = "" if page_num == 1 else f"?page={page_num}"
        url = f"{base_url}{query}"
        pages.append(url)
    return pages


def get_pod_urls(page_urls):
  pod_urls = []
  for page_url in page_urls:

    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.find_all("a", {"class": "hsp-card-episode"})
    page_urls = [f"https://www.happyscribe.com/{link.get('href')}" for link in links]
    
    for url in page_urls:
        pod_urls.append(url)
    
  return pod_urls


def scrape_happyscribe_pod(i, ):
  pass

def scrape_happyscribe():

    page_urls = get_page_urls()
    pod_urls = get_pod_urls(page_urls)

    for url in pod_urls:
        print(url)
    return

    # pool_size = 5
    # pool = Pool(pool_size)

    # LAST_EPISODE = 1571
    # for num in range(len(urls)):
    #     current  = LAST_EPISODE - num
    #     pool.apply_async(scrape_happyscribe_pod, (current, url))

    # pool.close()
    # pool.join()


if __name__ == '__main__':
    scrape_happyscribe()