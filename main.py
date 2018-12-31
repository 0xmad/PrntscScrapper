import os
import string
import argparse
from threading import Thread

from scrapper import Scrapper

code_chars = list(string.ascii_lowercase) + list(string.digits)
base = len(code_chars)

def digit_to_char(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)

def str_base(number, chars):
    if number < 0:
        return '-' + str_base(-number, chars)
    (d, m) = divmod(number, chars)
    if d > 0:
        return str_base(d, chars) + digit_to_char(m)
    return digit_to_char(m)

def next_code(curr_code, index):
    code_next = int(curr_code, base)
    return str_base(code_next + index + 1, base)

def scrap_pictures(scrapper, current_code, thread_index):
    while True:
        current_code = next_code(current_code, thread_index)
        img = scrapper.generate_random_url(current_code)
        scrapper.scrape(img)

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        help = 'The path where images will be stored.',
        default = './images'
    )
    parser.add_argument('--threads', help = 'The number of threads.', default = '1')
    parser.add_argument(
        '--code',
        help = '6 character string made up of lowercase letters and numbers which is where the '
               'scraper will start. e.g. abcdef -> abcdeg -> abcdeh',
        default = 'm1llk1'
    )

    args = parser.parse_args()
    image_path, count, arg_code = args.path, int(args.threads), args.code

    return image_path, count, arg_code

if __name__ == '__main__':
    path, thread_count, code = parse_command_line()

    if not os.path.exists(path):
        os.makedirs(path)

    picture_scrapper = Scrapper(path)
    threads = []

    try:
        for i in range(thread_count):
            thread = Thread(target = scrap_pictures, args = (picture_scrapper, code, i))
            thread.start()
            threads.append(thread)
    except KeyboardInterrupt:
        for t in threads:
            t.join(1)
