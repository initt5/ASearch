import os
import discord
import json
from discord.ext import tasks
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
    printer.start()
    print('We have logged in as {0.user}'.format(client))


@tasks.loop(minutes=30.0)
async def printer():
    settings_file = open('settings.json', encoding="utf-8")
    settings = json.load(settings_file)
    if not 'preferred_location' in settings:
        embed_list = create_embed('$find all')
    else:
        if 'price_bound' in settings:
            if 'meters_bound' in settings:
                embed_list = create_embed(
                    f"$find {settings['preferred_location']} {settings['price_bound']} {settings['meters_bound']}")
            else:
                embed_list = create_embed(f"$find {settings['preferred_location']} {settings['price_bound']}")
        else:
            embed_list = create_embed(f"$find {settings['preferred_location']}")
    channel = client.get_channel(int(os.getenv('CHANNEL_ID')))
    for embed in embed_list:
        await channel.send(embed=embed)


@client.event
async def on_message(message):
    if message.content.startswith('$settings'):
        settings_message = set_settings(message.content)
        await message.channel.send(embed=settings_message)
        return
    if not message.content.startswith('$find'):
        return
    if message.author == client.user:
        return

    embed_list = create_embed(message.content)
    if type(embed_list) == list:
        for embed in embed_list:
            await message.channel.send(embed=embed)
    else:
        await message.channel.send(embed=embed_list)


def create_embed(content):
    if content.startswith('$find'):
        embed = discord.Embed(title='Invalid arguments, try $find | location/all | max price | min living space ')
        message = content.split(' ')
        if message[0] != '$find' or len(message) == 1:
            return embed
        message_args = message[1:]
        loc = message_args[0].lower()
        if len(message_args) > 0 and loc in LOCATIONS:
            location_id = LOCATIONS[loc]

            if len(message_args) > 1 and message_args[1].isdigit():
                price_bound = message_args[1]
                if len(message_args) == 3 and message_args[2].isdigit():
                    meters_bound = message_args[2]
                    flat_list = FlatList(
                        f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bdistrict_id%5D={location_id}&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D={price_bound}&search%5Bfilter_float_m:from%5D={meters_bound}")
                else:
                    flat_list = FlatList(
                        f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bdistrict_id%5D={location_id}&search%5Border%5D=created_at:desc&search%5Bfilter_float_price:to%5D={price_bound}")
            else:
                flat_list = FlatList(
                    f"https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Bdistrict_id%5D={location_id}&search%5Border%5D=created_at:desc")
        elif loc == 'all':
            flat_list = FlatList(
                "https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/warszawa/?search%5Border%5D=created_at:desc")
        else:
            return embed
        flats = flat_list.get_list_of_flats()
        first_loc = parse_loc_and_date(flats[0].footer)['loc']
        embed_list = []
        for flat in flats:
            link = parse_link(flat.link)
            loc_and_date = parse_loc_and_date(flat.footer)
            if len(message_args) > 0 and loc_and_date['loc'] != first_loc and message_args[0] != 'all':
                break
            embed = discord.Embed(title=loc_and_date['loc'] + "| " + flat.price + " | " + flat.meters,
                                  description=link['description'],
                                  color=0xFF5733)
            embed.set_footer(text=link['title'] + "\n\n" + f"{loc_and_date['date']}")
            embed_list.append(embed)
        return embed_list


def set_settings(content):
    if content.startswith('$settings'):
        settings_file = open('settings.json', 'r+', encoding="utf-8")
        json.dump({}, settings_file)
        settings = {}
        embed = discord.Embed(title='Invalid arguments, try $settings | location/all | max price | min living space')
        message = content.split(' ')
        if message[0] != '$settings' or len(message) == 1:
            return embed
        message_args = message[1:]
        loc = message_args[0].lower()
        if len(message_args) > 0 and loc in LOCATIONS:
            embed = discord.Embed(title='Done')
            settings["preferred_location"] = loc
            if len(message_args) > 1 and message_args[1].isdigit():
                price_bound = message_args[1]
                settings["price_bound"] = price_bound
                if len(message_args) == 3 and message_args[2].isdigit():
                    meters_bound = message_args[2]
                    settings["meters_bound"] = meters_bound
        settings_file.seek(0)
        json.dump(settings, settings_file)
        settings_file.truncate()
        settings_file.close()
        return embed


client.run(os.getenv('TOKEN'))
