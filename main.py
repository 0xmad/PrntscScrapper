import sys
import getopt
import os
from threading import Thread

from scrapper import Scrapper

def scrap_pictures(scrapper):
    while True:
        img = scrapper.generate_random_url()
        scrapper.scrape(img)

def parse_command_line(argv):
    try:
        opts, args = getopt.getopt(argv, 'hp:t:', ['path=', 'threads='])

        image_path, count = './images', 1

        for opt, arg in opts:
            if opt == '-h':
                print()
                print(
                    'main.py -t <number of threads> -p <save path>',
                    '-t (--threads=) - number of threads (default 1)',
                    '-p (--path=) - path to save images (default ./image)',
                    sep = '\n\t'
                )
                sys.exit()
            elif opt in ('-p', '--path'):
                image_path = arg
            elif opt in ('-t', '--threads'):
                count = int(arg)

        return image_path, count
    except (ValueError, getopt.GetoptError):
        print('Error! See usage: main.py -h')
        sys.exit(2)

if __name__ == '__main__':
    path, thread_count = parse_command_line(sys.argv[1:])

    if not os.path.exists(path):
        os.makedirs(path)

    picture_scrapper = Scrapper(path)
    threads = []

    try:
        for _ in range(thread_count):
            thread = Thread(target = scrap_pictures, args = (picture_scrapper,))
            thread.start()
            threads.append(thread)
    except KeyboardInterrupt:
        for t in threads:
            t.join(1)
