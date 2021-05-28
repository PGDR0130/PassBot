import os
import discord
import sqlite3
import setRW  #read and write data functions
from keep_alive import keep_alive  #import the web server script
import threading
import sys

threads = []


def add_pass(user_id: int):  #for threading
    stage = 0 

    @client.event
    async def on_message(message):
        global stage
        stage = 0
        print("no")

        if message.author == user_id:
            print(stage)
            if message.content.startswith("#exit"):
                await message.channel.send("Exiting")
                sys.exit()
            
            stage += 1
            if stage == 50:
                sys.exit() 


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
            help = f.read()
            await message.channel.send(help)

    elif message.content.startswith('#addpass'):
        threading.Thread(target=add_pass,args=[message.author]).start()

    elif message.content.startswith('#deletepass'):
        pass

    else:
        print(threading.active_count())


#keep_alive() must be in front of the client.run(), otherwise it won't run.
keep_alive()
client.run(os.getenv('TOKEN'))
