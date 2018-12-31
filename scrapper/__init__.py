import os
import urllib.error
import urllib.request
import random
import string

from bs4 import BeautifulSoup

class Scrapper:
    _empty_file_sizes = [0, 4275]
    _url = 'https://prnt.sc'
    _path = './images'

    def __init__(self, path):
        if path is not None:
            self._path = path

    def generate_random_url(self):
        possible_chars = string.digits + string.ascii_lowercase
        slug = ''.join(random.choice(possible_chars) for _ in range(6))

        return { 'url': f'{self._url}/{slug}.png', 'name': f'{slug}.png' }

    def scrape(self, img):
        try:
            filename = f'''{self._path}/{img['name']}'''
            fake_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0 '
            headers = {
                'User-agent': fake_agent
            }
            request = urllib.request.Request(
                img['url'],
                headers = headers,
            )

            response = urllib.request.urlopen(request)
            html = response.read()
            soup = BeautifulSoup(str(html))
            image = soup.find(id = 'screenshot-image')
            src = image.get('src')

            urllib.request.urlretrieve(src, filename)

            file_size = os.path.getsize(filename)

            if file_size in self._empty_file_sizes:
                print(f'''[-] Invalid image url {img['url']}''')
                os.remove(filename)
                return 404
            else:
                print(f'''[+] Valid image url {img['url']}''')
        except urllib.error.HTTPError as e:
            print(f'''[-] {e} - {img['url']}''')
            return e.code
        except (urllib.error.ContentTooShortError, ValueError):
            return 400

        return 200
