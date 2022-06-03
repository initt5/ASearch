import os
from datetime import datetime
import discord
from dotenv import load_dotenv
from scrap import FlatList, parse_link, parse_loc_and_date


load_dotenv()

client = discord.Client()

LOCATIONS = {'bemowo': 367, 'białołęka': 365, 'bialoleka': 365, 'bielany': 369, 'mokotów': 353, 'mokotow': 353,
             'ochota': 355, 'praga południe': 381, 'praga-południe': 381, "praga-poludnie": 381, "praga poludnie": 381,
             'praga polnoc': 379, 'praga-północ': 379, "praga-polnoc": 379, "praga północ": 379, 'rembertów': 361,
             'rembertow': 361, 'śródmieście': 351, 'srodmiescie': 351, 'targowek': 377, "targówek": 377, 'ursus': 371,
             'ursynów': 373, 'ursynow': 373, 'wawer': 383, 'wesoła': 533, 'wesola': 533, 'wilanów': 375, 'wilanow': 375,
             'włochy': 357, 'wlochy': 357, 'wola': 359, 'żoliborz': 363, 'zoliborz': 363}


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$find'):
        message_args = message.content.split(' ')[1:]
        if len(message_args) == 1 and message_args[0] in LOCATIONS:
            location_id = LOCATIONS[message_args[0]]
            flat_list = FlatList(
                f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bdistrict_id%5D={location_id}&search%5Border%5D=created_at:desc")
        elif len(message_args) == 2 and message_args[0] in LOCATIONS and message_args[1].isdigit():
            location_id = LOCATIONS[message_args[0]]
            price_bound = message_args[1]
            flat_list = FlatList(
                f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bdistrict_id%5D={location_id}&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D={price_bound}")
        elif len(message_args) == 3 and message_args[0] in LOCATIONS and message_args[1].isdigit() and message_args[2].isdigit():
            location_id = LOCATIONS[message_args[0]]
            price_bound = message_args[1]
            meters_bound = message_args[2]
            flat_list = FlatList(
                f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bdistrict_id%5D={location_id}&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D={price_bound}&search%5Bfilter_float_m:to%5D={meters_bound}")
        elif len(message_args) == 0 or message_args[0] == 'all':
            flat_list = FlatList(
                "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Border%5D=created_at:desc")
        else:
            await message.channel.send('Invalid arguments')
            return
        flats = flat_list.get_list_of_flats()
        for flat in flats:
            link = parse_link(flat.link)
            loc_and_date = parse_loc_and_date(flat.footer)
            embed = discord.Embed(title=loc_and_date['loc'] + "| " + flat.meters + " | " + flat.price,
                                  description=link['description'],
                                  color=0xFF5733)
            embed.set_footer(text=link['title'] + "\n\n" + f"{loc_and_date['date']}")
            await message.channel.send(embed=embed)


client.run(os.getenv('TOKEN'))
