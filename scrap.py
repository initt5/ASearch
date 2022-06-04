from bs4 import BeautifulSoup
import requests


class FlatList:
    def __init__(self, url):
        self.URL = url
        self.page = requests.get(self.URL)
        self.soup = BeautifulSoup(self.page.content, "html.parser")

    def get_list_of_flats(self):
        links = self.soup.find_all("a", {"class": "css-1bbgabe"})
        flat_list = []
        for link in links:
            link_url = link['href']
            payed = False
            footer = link.find('p', {"class": "css-p6wsjo-Text eu5v0x0"}).getText()
            meters = link.find('p', {"class": "css-1bhbxl1-Text eu5v0x0"}).getText()
            price = link.find('p', {"class": "css-l0108r-Text eu5v0x0"}).getText().replace('do negocjacji', ' do negocjacji')
            if link.find('div', {'class': "css-1katuj6"}):
                payed = True
            flat = Flat(link_url, footer, meters, price, payed)
            flat_list.append(flat)
        return flat_list


class Flat:
    def __init__(self, link, footer, meters, price, payed):
        self.link = link
        self.footer = footer
        self.meters = meters
        self.price = price
        self.payed = payed


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
