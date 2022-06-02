from bs4 import BeautifulSoup
import requests


class FlatList:
    def __init__(self):
        self.URL = "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Border%5D=created_at:desc"
        self.page = requests.get(self.URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.urlList = []

    def get_list_of_flats(self):
        results = self.soup.find_all("a", {"class": "css-1bbgabe"})
        for result in results:
            link_url = result['href']
            cleared_link = self.clear_link(link_url)
            self.urlList.append(cleared_link)
        print(self.urlList)
        return results

    def clear_link(self, link):
        good_link = link.split('/')[3][:-5]
        return good_link


flats = FlatList()
flats.get_list_of_flats()
