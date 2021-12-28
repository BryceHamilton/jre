import requests
from datetime import datetime
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool as Pool

from file_writers import write_all


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_title(soup):
    title = soup.find("h1", {"id": "episode-title"}).get_text()
    return title


def get_pod_num(title):
    splitter = "with " if "MMA" in title else " - "

    if "Companion" in title:
        pod_num = "Fight_Companion"
    else:
        pod_num = title.split(splitter)[0]
        pod_num = pod_num.split("#")[1].strip()
        if "MMA" in title:
            pod_num = f"MMA_{pod_num}"

    return pod_num


def get_guest(title):
    splitter = "with " if "MMA" in title else " - "
    guest = title.split(splitter)[1]
    return guest


def get_guest_desc(soup):
    guest_desc = soup.find("div", {"id": "description"}).get_text()
    return guest_desc.strip().replace('\\', '')


def get_date(soup):
    episode_info = soup.find("div", {"class": "hsp-episode-info"})
    date_raw = episode_info.find(
        "li", {"class": "hs-font-positive small-base date"}
    ).get_text()
    date_obj = datetime.strptime(date_raw.strip(), "%d %b %Y")
    date = date_obj.strftime("%B %d, %Y")
    return date


def get_transcript(soup):
    paragraphs = soup.find_all("p", {"class": "hsp-paragraph-words"})
    doc_list = [p.get_text() for p in paragraphs]
    transcript = " ".join(doc_list).replace('\\', '')
    return transcript


def get_page_urls():
    BASE_URL = "https://www.happyscribe.com/public/the-joe-rogan-experience"
    pages = []
    for page_num in range(1, 8):
        query = "" if page_num == 1 else f"?page={page_num}"
        url = f"{BASE_URL}{query}"
        pages.append(url)
    return pages


def get_pod_urls(page_urls):
    BASE_URL = "https://www.happyscribe.com"
    pod_urls = []
    for page_url in page_urls:

        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")

        links = soup.find_all("a", {"class": "hsp-card-episode"})

        page_urls = [
            f"{BASE_URL}/{link.get('href')}"
            for link in links
            if "Elon Musk Talks About Colonizing the Galaxy" not in link.get_text()
        ]

        for url in page_urls:
            pod_urls.append(url)

    return pod_urls


def scrape_happyscribe_pod(url,):
    soup = get_soup(url)

    date = get_date(soup)
    guest_desc = get_guest_desc(soup)

    title = get_title(soup)
    if '-' not in title and 'MMA' not in title:
        return

    pod_num = get_pod_num(title)
    guest = get_guest(title)

    transcript = get_transcript(soup)

    write_all(pod_num, guest_desc, date, guest, transcript)


def scrape_happyscribe(pool_size):

    page_urls = get_page_urls()
    pod_urls = get_pod_urls(page_urls)

    pool = Pool(pool_size)

    for url in pod_urls:
        pool.apply_async(scrape_happyscribe_pod, (url,))

    pool.close()
    pool.join()


if __name__ == "__main__":
    scrape_happyscribe(pool_size=10)
