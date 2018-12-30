import os
import random
import string
import urllib.error
import urllib.request

class Scrapper:
    # need to define empty sizes if imgur doesn't have the image
    empty_file_sizes = [0, 503, 4939, 4940, 4941, 12003, 5556]
    url = 'https://i.imgur.com'
    path = './images'

    def __init__(self, path):
        if path is not None:
            self.path = path

    def generate_random_url(self):
        possible_chars = string.ascii_uppercase + string.digits + string.ascii_lowercase

        # id length 6 or 7
        current_length = random.randint(6, 8)

        slug = ''.join(random.choice(possible_chars) for _ in range(current_length))

        return { 'url': f'{self.url}/{slug}.jpg', 'name': f'{slug}.jpg' }

    def scrape(self, img):
        try:
            filename = f'''{self.path}/{img['name']}'''
            urllib.request.urlretrieve(img['url'], filename)
            file = os.path.getsize(filename)

            if file in self.empty_file_sizes:
                print(f'''[-] Invalid image url {img['url']}''')
                os.remove(filename)
                return 404
            else:
                print(f'''[+] Valid image url {img['url']}''')
        except urllib.error.HTTPError:
            return 404
        except urllib.error.ContentTooShortError:
            return 400

        return 200
