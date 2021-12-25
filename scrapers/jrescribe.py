import os
import requests
from multiprocessing.pool import ThreadPool as Pool
from bs4 import BeautifulSoup

def get_abs_path(dir):
    curr_dir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(curr_dir, dir))


def scrape_jrescribe_pod(pod_num):
    URL = f"https://jrescribe.com/transcripts/p{pod_num}.html"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    p_tags = soup.find_all("p")
    doc_list = [p.get_text() for p in p_tags]
    doc = " ".join(doc_list)
    doc_no_footer = doc.split("Help improve this transcript!")[1]

    title = soup.find("h1").get_text()
    splitter = "with " if "MMA" in title else " - "
    guest = title.split(splitter)[1]

    file_name = f"{pod_num}.txt"

    guests_dir = get_abs_path("guests")
    guest_file_path = os.path.join(guests_dir, file_name)
    with open(guest_file_path, "w") as f:
        f.write(guest)

    transcripts_dir = get_abs_path("transcripts")
    transcript_file_path = os.path.join(transcripts_dir, file_name)
    with open(transcript_file_path, "w") as f:
        f.write(doc_no_footer)

def scrape_jrescribe(pool_size):
    POD_START = 1104
    POD_END = 1266

    pool = Pool(pool_size)

    for num in range(POD_START, POD_END):
        pool.apply_async(scrape_jrescribe_pod, (num,))

    pool.close()
    pool.join()
