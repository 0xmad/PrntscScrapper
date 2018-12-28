import sys
import concurrent.futures

from scrapper import Scrapper

def scrap_pictures(scrapper):
    while True:
        scrapper.generate_random_url()
        scrapper.scrape()

path = sys.argv[1] if len(sys.argv) > 1 else None

picture_scrapper = Scrapper(path)

try:
    with concurrent.futures.ThreadPoolExecutor(1) as executor:
        executor.submit(scrap_pictures, picture_scrapper)
except:
    sys.exit(-1)

