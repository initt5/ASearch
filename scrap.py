from bs4 import BeautifulSoup
import requests


class FlatList:
    def __init__(self):
        self.URL = "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Border%5D=created_at:desc"
        self.page = requests.get(self.URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def get_list_of_flats(self):
        links = self.soup.find_all("a", {"class": "css-1bbgabe"})
        flat_list = []
        for link in links:
            link_url = link['href']
            footer = link.find('p', {"class": "css-p6wsjo-Text eu5v0x0"}).getText()
            flat = Flat(link_url, footer)
            flat_list.append(flat)

        return flat_list


class Flat:
    def __init__(self, link, footer):
        self.link = link
        self.footer = footer


def parse_link(link):
    data = {}
    if link.startswith('/d/'):
        data['description'] = f"[OLX](https://www.olx.pl{link})"
        pre_title = link.split('/')[3]
        data['title'] = ' '.join(pre_title.split('-')[:-2]).capitalize()
    else:
        data['description'] = f"[OTODOM]({link})"
        pre_title = link.split('/')[5]
        data['title'] = ' '.join(pre_title.split('-')[:-1]).capitalize()
    return data


def parse_loc_and_date(loc_and_date):
    split_loc_and_date = loc_and_date.replace('Warszawa, ', '').split('-')
    if 'Praga' in loc_and_date:
        loc = split_loc_and_date[0] + '-' + split_loc_and_date[1]
        date = split_loc_and_date[2].replace('Odświeżono', '')
    else:
        loc = split_loc_and_date[0]
        date = split_loc_and_date[1].replace('Odświeżono', '')
    loc_date_data = {'loc': loc, 'date': date.strip()}
    return loc_date_data
