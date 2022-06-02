from bs4 import BeautifulSoup
import requests


class FlatList:
    def __init__(self):
        self.URL = "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Border%5D=created_at:desc"
        self.page = requests.get(self.URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def get_list_of_flats(self):
        results = self.soup.find_all("a", {"class": "css-1bbgabe"})
        url_list = []
        for result in results:
            link_url = result['href']
            cleared_link = self.clear_link(link_url)
            url_list.append(cleared_link)
        return url_list

    def clear_link(self, link):
        i = 0
        if "otodom" in link:
            i = 5
        else:
            i = 3
        good_link = link.split('/')[i]
        return good_link


flats = FlatList()
flats.get_list_of_flats()
