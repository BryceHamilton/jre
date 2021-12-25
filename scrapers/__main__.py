import os
import time
from jrescribe import scrape_jrescribe
from happyscribe import scrape_happyscribe


def scrape_all(pool_size):
    scrape_jrescribe(pool_size)
    scrape_happyscribe(pool_size)


if __name__ == "__main__":

    thread_count = 10

    start = time.time()
    scrape_all(thread_count)
    end = time.time()

    curr_dir = os.path.dirname(__file__)
    file_name = f"{thread_count}_threads.txt"
    log_folder_path = os.path.abspath(os.path.join(curr_dir, "logs"))
    log_file_path = os.path.join(log_folder_path, file_name)

    with open(log_file_path, "w") as f:
        f.write(str(end - start))
