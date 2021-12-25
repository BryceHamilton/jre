from multiprocessing.pool import ThreadPool as Pool
import requests
from bs4 import BeautifulSoup


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
        page_urls = [
            f"https://www.happyscribe.com/{link.get('href')}" for link in links
        ]

        for url in page_urls:
            pod_urls.append(url)

    return pod_urls


def scrape_happyscribe_pod(
    url,
):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("h1", {"id": "episode-title"}).get_text()

    splitter = "with " if "MMA" in title else " - "

    pod_num, guest = title.split(splitter)
    pod_num = pod_num.split("#")[1].strip()

    if "MMA" in title:
        pod_num = f"MMA_{pod_num}"
    elif "Companion" in title:
        pod_num = "Fight_Companion"

    paragraphs = soup.find_all("p", {"class": "hsp-paragraph-words"})
    doc_list = [p.get_text() for p in paragraphs]
    doc = " ".join(doc_list)

    with open(f"guests/{pod_num}.txt", "w") as f:
        f.write(guest)

    with open(f"transcripts/{pod_num}.txt", "w") as f:
        f.write(doc)


def scrape_happyscribe(pool_size):

    page_urls = get_page_urls()
    pod_urls = get_pod_urls(page_urls)

    pool = Pool(pool_size)

    for url in pod_urls:
        pool.apply_async(scrape_happyscribe_pod, (url,))

    pool.close()
    pool.join()


if __name__ == "__main__":
    scrape_happyscribe()
