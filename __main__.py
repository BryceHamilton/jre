from jrescribe import scrape_jrescribe
from happyscribe import scrape_happyscribe

def scrape_all():
  scrape_jrescribe()
  scrape_happyscribe()


if __name__ == '__main__':
  scrape_happyscribe()
