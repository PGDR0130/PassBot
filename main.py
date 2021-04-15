import os
import discord
from keep_alive import keep_alive #import the web server script

client = discord.Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return None

    else :
        await message.channel.send(message.content)




#keep_alive() must be in front of the client.run(), otherwise it won't run.
keep_alive()
client.run(os.getenv('TOKEN'))