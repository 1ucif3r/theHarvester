from discovery.constants import *
from lib.core import *
from parsers import intelxparser
import requests
import time

class search_intelx:

    def __init__(self, word, limit):
        self.word = word
        # default key is public key
        self.key = Core.intelx_key()
        if self.key is None:
            raise MissingKey(True)
        self.database = 'https://public.intelx.io/'
        self.results = None
        self.info = ()
        self.limit = limit

    def do_search(self):
        try:
            user_agent = Core.get_user_agent()
            headers = {'User-Agent': user_agent, 'x-key': self.key}
            data = f'{{"term": "{self.word}", "maxresults": {self.limit}, "media": 0, "sort": 2 , "terminate": []}}'
            # data is json that corresponds to what we are searching for, sort:2 means sort by most relevant
            r = requests.post(f'{self.database}phonebook/search', data=data, headers=headers)
            if r.status_code == 400:
                raise Exception('Invalid json was passed in.')
            time.sleep(1)
            # grab uuid to send get request to fetch data
            uuid = r.json()['id']
            url = f'{self.database}phonebook/search/result?id={uuid}&offset=0&limit={self.limit}'
            r = requests.get(url, headers=headers)
            # to add in future grab status from r.text and check if more results can be gathered
            if r.status_code != 200:
                raise Exception('Error occurred while searching intelx.')
            self.results = r.json()
        except Exception as e:
            print(f'An exception has occurred: {e}')

    def process(self):
        print('\t Processing Results')
        self.do_search()
        intelx_parser = intelxparser.Parser()
        self.info = intelx_parser.parse_dictionaries(self.results)
        # Create parser and set self.info to tuple returned from parsing text.
        print('\t Done Searching Results')

    def get_emails(self):
        return self.info[0]

    def get_hostnames(self):
        return self.info[1]

