import os
import discord
import sqlite3
import setRW  #read and write data functions
from keep_alive import keep_alive  #import the web server script

client = discord.Client()

in_event = [] #add in the id if user is  

async def add_reactions(message, emojis):
    await message.add_reaction(emojis)





@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print()

@client.event
async def on_message(message):


    channel =  message.channel
    author = message.author.id

    if message.content == "#end_session":
        if author in in_event:
            in_event.pop(in_event.index(author))
        await add_reactions(message, "✅")
        await channel.send("Ended...")
        return 
    
    def check_session(id):
        if id in in_event:
            return True
        else:
            return False


    def add_check(m):
        return m.channel == channel and m.author.id == author 

    if message.author == client.user or message.author.id in in_event:#if the bot or the user is still in event return  
        return                                                        #阻擋器人自己的訊息和已經在儲存密碼的人 
        
    elif message.content.startswith("#list_settings"):
        with open('help_content.txt', 'r') as f:
            help = f.read()
            await message.channel.send(help)

    elif message.content.startswith('#addpass'):  #add password command
        in_event.append(message.author.id)

        a = await channel.send("Please enter the name or the url of the site")
        site_url = await client.wait_for('message', check=add_check)
        await site_url.delete()
        await add_reactions(a, "✅")

        b = await channel.send("Please enter the password that you want to store ")
        site_pass = await client.wait_for('message', check=add_check)
        await site_pass.delete()
        await add_reactions(b, "✅")
            
        c = await channel.send("Please enter the password for the encryption ")
        master_pass = await client.wait_for('message', check=add_check)
        await master_pass.delete()
        await add_reactions(c, "✅")

        await channel.send("Done collecting information")
        
            
        in_event.pop(in_event.index(author))





    elif message.content.startswith('#deletepass'):
        pass

    else:
        await message.channel.send(message.content)
        print(in_event)





#keep_alive() must be in front of the client.run(), otherwise it won't run.
keep_alive()
client.run(os.getenv('TOKEN'))
