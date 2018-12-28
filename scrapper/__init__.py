import os
import random
import string
import urllib.error
import urllib.request

class Scrapper:
    img = { }
    # need to define empty sizes if imgur doesn't have the image
    empty_file_sizes = [0, 503, 4939, 4940, 4941, 12003, 5556]
    url = 'https://i.imgur.com'
    path = '.'

    def __init__(self, path):
        if path is not None:
            self.path = path

    def generate_random_url(self):
        # 5 or 6 length for image id
        amount = random.randint(5, 7)

        seed = string.ascii_uppercase + string.digits + string.ascii_lowercase
        image_id = ''.join((random.choice(seed) for _ in range(amount)))

        self.img = { 'url': f'{self.url}/{image_id}.jpg', 'name': f'{image_id}.jpg' }

    def scrape(self):
        try:
            filename = f'''{self.path}/{self.img['name']}'''
            urllib.request.urlretrieve(self.img['url'], filename)
            file = os.path.getsize(self.img['name'])

            if file in self.empty_file_sizes:
                print('Invalid image url')
                os.remove(filename)
                return 404
            else:
                print(f'Valid image url {self.img}')
        except urllib.error.HTTPError:
            return 404
        except urllib.error.ContentTooShortError:
            return 400
        finally:
            self.img = { }

        return 200
