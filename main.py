import discord
from setRW import setting_data #read and write data functions
from keep_alive import keep_alive  #import the web server script
import edcode
import sql_handler as sqlh
import asyncio

client = discord.Client()
line = '-'*50

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


    def _check(m):
        return m.channel == channel and m.author.id == author 

    if message.author == client.user or message.author.id in in_event:#if the bot or the user is still in event return  
        return                                                        #阻擋器人自己的訊息和已經在儲存密碼的人 
        
    elif message.content.startswith("#help"):
        with open('help_content.txt', 'r') as f:
            help = f.read()
            await message.channel.send(help)



    #add password session
    elif message.content.startswith('#addpass'):  #add password command
        await channel.send(line)
        in_event.append(author)

        a = await channel.send("Please enter the name or the url of the site")
        site_url = await client.wait_for('message', check=_check)
        await site_url.delete()
        await add_reactions(a, "✅")

        b = await channel.send("Please enter the password that you want to store ")
        site_pass = await client.wait_for('message', check=_check)
        await site_pass.delete()
        await add_reactions(b, "✅")
            
        c = await channel.send("Please enter the password for the encryption ")
        master_pass = await client.wait_for('message', check=_check)
        await master_pass.delete()
        await add_reactions(c, "✅")

        await channel.send("Done collecting information")
        
        encoded_pass = edcode.encode(int(master_pass.content), site_pass.content)
        result = sqlh.write_pass(author, site_url.content, encoded_pass)
        await channel.send(result)
        await channel.send(line)

            
        in_event.pop(in_event.index(author))




    #find password session 
    elif message.content.startswith("#findpass"):
        in_event.append(author)

        a = await channel.send("Plesae enter the site or url that you want to find.")
        site_url = await client.wait_for('message', check=_check)
        await site_url.delete()
        await add_reactions(a, "✅")

        b = await channel.send("Please enter the password for the decryption")
        master_pass = await client.wait_for('message', check=_check)
        await master_pass.delete()
        await add_reactions(b, "✅")

        await channel.send("Done collecting information")
        decoded_pass = edcode.decode(int(master_pass.content), sqlh.read_pass(author,site_url.content))


        
        send_pass = await channel.send(str(decoded_pass))
        await asyncio.sleep(int(setting_data.find(author, 'delete_time'))) #wait for _ seconds and than delete
        await send_pass.delete() 
        in_event.pop(in_event.index(author))    




    elif message.content.startswith('#deletepass'):
        in_event.append(author)
        a = await channel.send("Plesae enter the site or url that you want to delete")
        site_url = await client.wait_for('message', check=_check)
        result = sqlh.delete_pass(author, site_url.content)
        await channel.send(result)
        in_event.pop(in_event.index(author))




    elif message.content.startswith('#listSettings'):
        await channel.send(setting_data.find(author, 'all'))



    elif message.content.startswith('#settingChange'):
        in_event.append(author)
        await channel.send('what option in the setting do you want to change')
        option = await client.wait_for('message', check=_check)
        await channel.send('what do you want to change to')
        content = await client.wait_for('message', check=_check)
        result = setting_data.replace(author, option.content, content.content)
        await channel.send(result)

        in_event.pop(in_event.index(author))

    else:
        await message.channel.send(message.content)
        print(in_event)





#keep_alive() must be in front of the client.run(), otherwise it won't run.
keep_alive()
client.run(os.getenv('TOKEN'))
