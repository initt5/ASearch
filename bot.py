import os
import discord
from dotenv import load_dotenv
from scrap import FlatList


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
        links = flat_list.get_list_of_flats()
        embed = discord.Embed()
        for link in links:
            embed = discord.Embed(title="Sample Embed",
                                  description=f"[OLX](https://www.olx.pl/d/oferta/{link})",
                                  color=0xFF5733)
            await message.channel.send(embed=embed)

client.run(os.getenv('TOKEN'))
