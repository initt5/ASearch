import os
import discord
from dotenv import load_dotenv
from scrap import FlatList


load_dotenv()

client = discord.Client()


def get_data(link):
    data = {}
    if link.startswith('/d/'):
        data['description'] = f"[OLX](https://www.olx.pl{link})"
        pre_title = link.split('/')[3]
        data['title'] = ' '.join(pre_title.split('-')[:-2]).capitalize()
    else:
        data['description'] = f"[OLX]({link})"
        pre_title = link.split('/')[5]
        print(pre_title)
        data['title'] = ' '.join(pre_title.split('-')[:-1]).capitalize()
    return data
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$all'):
        flat_list = FlatList()
        links = flat_list.get_list_of_flats()
        embed = discord.Embed()
        for link in links:
            data = get_data(link)
            embed = discord.Embed(title=data['title'],
                                  description=data['description'],
                                  color=0xFF5733)
            await message.channel.send(embed=embed)

client.run(os.getenv('TOKEN'))
