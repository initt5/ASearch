import os
from datetime import datetime
import discord
from dotenv import load_dotenv
from scrap import FlatList, parse_link, parse_loc_and_date


load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$all'):
        flat_list = FlatList()
        flats = flat_list.get_list_of_flats()
        for flat in flats:
            link = parse_link(flat.link)
            loc_and_date = parse_loc_and_date(flat.footer)
            embed = discord.Embed(title=loc_and_date['loc'],
                                  description=link['description'],
                                  color=0xFF5733)
            embed.set_footer(text=link['title'] + "\n\n" + f"{loc_and_date['date']}")
            await message.channel.send(embed=embed)


client.run(os.getenv('TOKEN'))
