import unittest
import requests
import time
from dotenv import dotenv_values

config = dotenv_values(".env")
#ENDPOINT = 'http://127.0.0.1:5000'
ENDPOINT = 'http://192.144.14.9:8000'
#ENDPOINT = 'http://192.144.14.9:5000'
HEADERS = {"Authorization": f"Bearer {config['APP_TOKEN']}"}


class TestApi(unittest.TestCase):
    def test_home(self):
        t0 = time.time()
        resp = requests.get(ENDPOINT)
        self.assertIn('Housing price service', resp.text)
        t1 = time.time()
        print(f'test home: {t1-t0} s')

    def test_api(self):
        t0 = time.time()
        data = {'area': 42}
        resp = requests.post(ENDPOINT +'/predict',
                             json=data,
                             headers=HEADERS)
        t1 = time.time()
        print(f'test predict: {t1 - t0} s')
        self.assertIn('price', resp.text)


if __name__ == '__main__':
    unittest.main()
