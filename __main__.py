import os
import time
from jrescribe import scrape_jrescribe
from happyscribe import scrape_happyscribe


def scrape_all(pool_size):
    scrape_jrescribe(pool_size)
    scrape_happyscribe(pool_size)


def clean(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def clean_all():
    clean("transcripts")
    clean("guests")


if __name__ == "__main__":

    thread_count = 5

    start = time.time()
    scrape_all(thread_count)
    end = time.time()

    with open(f"logs/{thread_count}_threads.txt", "w") as f:
        f.write(str(end - start))
