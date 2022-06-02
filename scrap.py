from bs4 import BeautifulSoup
import requests


class FlatList:
    def __init__(self):
        self.URL = "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Border%5D=created_at:desc"
        self.page = requests.get(self.URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.url_list = []

    def get_list_of_flats(self):
        results = self.soup.find_all("a", {"class": "css-1bbgabe"})
        url_list = []
        for result in results:
            link_url = result['href']
            url_list.append(link_url)
        return url_list


flats = FlatList()
flats.get_list_of_flats()
