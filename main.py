import os
import discord
from keep_alive import keep_alive  #import the web server script
import sqlite3
import setRW

client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return None
    
    
    elif message.content.startswith("#list_settings"):
        with open('help_content.txt', 'r') as f:
            mes = f.read()
            await message.channel.send(mes)
    
    elif message.content.startswith('#addpass'):
        pass
    
    elif message.content.startswith('#deletepass'):
        pass

    
    else:
        await message.channel.send(message.content)


#keep_alive() must be in front of the client.run(), otherwise it won't run.
keep_alive()
client.run(os.getenv('TOKEN'))