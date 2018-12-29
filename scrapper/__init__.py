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
        # 5 or 6 length for image id
        amount = random.randint(5, 7)

        seed = string.ascii_uppercase + string.digits + string.ascii_lowercase
        image_id = ''.join((random.choice(seed) for _ in range(amount)))

        return { 'url': f'{self.url}/{image_id}.jpg', 'name': f'{image_id}.jpg' }

    def scrape(self, img):
        try:
            filename = f'''{self.path}/{img['name']}'''
            urllib.request.urlretrieve(img['url'], filename)
            file = os.path.getsize(filename)

            if file in self.empty_file_sizes:
                print('[-] Invalid image url')
                os.remove(filename)
                return 404
            else:
                print(f'''[+] Valid image url {img['url']}''')
        except urllib.error.HTTPError:
            return 404
        except urllib.error.ContentTooShortError:
            return 400

        return 200
