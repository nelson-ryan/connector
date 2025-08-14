import requests
import json
from connector.config import NYT_BASEURL
from db.mysql_repository import MysqlRepository as ActiveRepository
from utils.utils import validate_print_date


class Scraper():
    BASEURL = NYT_BASEURL

    def __init__(self, print_date : str):

        validate_print_date(print_date)
        self.print_date = print_date

        self.url = self.BASEURL + print_date + ".json"

    def _get_web_puzzle(self):
        """Retrieves the given date's puzzle file from New York Times.
           The file is json-formatted text.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except Exception as e:
            raise e
        return response.json()
    
    @property
    def nyjson(self) -> dict:
        return self._get_web_puzzle()


class GoldenRetriever(ActiveRepository, Scraper):
    def __init__(self, print_date : str):

        ActiveRepository.__init__(self)
        Scraper.__init__(self, print_date)

    def fetch_puzzle(self):
        # TODO retrieve from DB first; pull from web if not present
        puzzlefromrepo = None # self.retrieve_stored_puzzle(self.print_date)
        return puzzlefromrepo if puzzlefromrepo else self._get_web_puzzle()

    @property
    def nyjson(self) -> dict:
        return self.fetch_puzzle()

    def _store_puzzle(self):
        raise NotImplementedError


