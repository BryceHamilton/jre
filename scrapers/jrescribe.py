import requests
from multiprocessing.pool import ThreadPool as Pool
from bs4 import BeautifulSoup

from file_writers import write_all


def get_soup(pod_num):
    if pod_num == 1210:
        pod_num = str(pod_num) + "a"

    URL = f"https://jrescribe.com/transcripts/p{pod_num}.html"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_guest_desc(soup):
    header = soup.find("div", {"class": "episode-header"})
    guest_desc = header.find("p").get_text()
    return guest_desc


def get_date(soup):
    header = soup.find("div", {"class": "episode-header"})
    date = header.find("h3").get_text()
    return date


def get_transcript(soup):
    p_tags = soup.find_all("p")
    doc_list = [p.get_text() for p in p_tags]
    doc = " ".join(doc_list)
    transcript = doc.split("Help improve this transcript!")[1]
    return transcript


def get_guest(soup):
    title = soup.find("h1").get_text()
    splitter = "with " if "MMA" in title else " - "
    guest = title.split(splitter)[1]
    return guest


def scrape_jrescribe_pod(pod_num):

    soup = get_soup(pod_num)
    guest_desc = get_guest_desc(soup)

    date = get_date(soup)
    transcript = get_transcript(soup)
    guest = get_guest(soup)

    write_all(pod_num, guest_desc, date, guest, transcript)


def scrape_jrescribe(pool_size):

    POD_START = 1104
    POD_END = 1266

    pool = Pool(pool_size)

    for num in range(POD_START, POD_END):
        pool.apply_async(scrape_jrescribe_pod, (num,))

    pool.close()
    pool.join()


if __name__ == "__main__":
    scrape_jrescribe(pool_size=10)
