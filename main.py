#一個可以儲存密碼的Discord bot --> Passbot
#109-2 自主學習

import discord
#Json 讀取寫入
from setRW import setting_data 
#加入讓程式維持運行的網站
from keep_alive import keep_alive 
import edcode
#sqlite 讀寫
import sql_handler as sqlh
import asyncio
import os

client = discord.Client()
line = '-'*50

 #確認使用者是不是在階段內
in_event = [] 
pending = {}

async def add_reactions(message, emojis):
    await message.add_reaction(emojis)

def is_number(text):
    return text.content.isnumeric()

#階段完成或錯誤的時候，清理資訊的函數
def end_session(m, mode): #mode0-user_end, mode1-Error_end
    if m.author.id in in_event:
        in_event.pop(in_event.index(m.author.id))
    if mode == 0 :
        for i in pending[f'{m.author.id}']:
            i.close()
        pending[f'{m.author.id}'] = []
        return "Ended"

    


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(client.is_ws_ratelimited())
    if client.is_ws_ratelimited() == True :
        return
    print()
    

@client.event
async def on_message(message):
    try:

        channel =  message.channel
        author = message.author.id

        if message.content == "#end_session":
            end_session(message, 0)
            await add_reactions(message, "✅")
            return 
        
        def check_session(id):
            return True if id in in_event else False

        def _check(m):
            return m.channel == channel and m.author.id == author and not m.content.startswith("#end_session")
        
        # 阻擋機器人自己的訊息
        if message.author == client.user: 
            return 
        
        #阻擋在階段內的使用者
        if message.author.id in in_event:
            return        

        #排出私訊訊息，因為私訊不能刪除紀錄
        if message.channel.type == discord.ChannelType.private:
            await message.channel.send("對不起，不支援私訊")
            return                         

        pending[f'{author}'] = []
        
        if message.content.startswith("#help"):
            with open('help_content.txt', 'r') as f:
                help = f.read()
                await message.channel.send(f'```{help}```')

        elif message.content.startswith("#passlist"):
            allpass = sqlh.read_pass(author, 'all')
            await message.channel.send(allpass)

        #add password session
        elif message.content.startswith('#addpass'):  #add password command
            await channel.send(line)
            in_event.append(author)

            #Please enter the name or the url of the site
            a = await channel.send("網站名子")
            pending[f'{author}'].append(client.wait_for('message', check=_check))
            site_url = await pending[f'{author}'][0]
            await site_url.delete()
            await add_reactions(a, "✅")

            b = await channel.send("請輸入要儲存的密碼")#Please enter the password that you want to store
            pending[f'{author}'].append(client.wait_for('message', check=_check))
            site_pass = await pending[f'{author}'][1]
            await site_pass.delete()
            await add_reactions(b, "✅")
                
            c = await channel.send("請輸入加密密碼(ONLY NUMBERS)")
            pending[f'{author}'].append(client.wait_for('message', check=_check))
            master_pass = await pending[f'{author}'][2]
            await master_pass.delete()

            if is_number(master_pass):
                await add_reactions(c, "✅")
            else:
                await add_reactions(c, "❌")
                await channel.send("對不起僅限數字")
                await channel.send(line)
                end_session(message, 1)
                return 

            await channel.send("完成資料收集")#Done collecting information
            
            encoded_pass = edcode.encode(int(master_pass.content), site_pass.content)
            result = sqlh.write_pass(author, site_url.content, encoded_pass)
            await channel.send(result)
            await channel.send(line)

                
            in_event.pop(in_event.index(author))


        #find password 
        elif message.content.startswith("#findpass"):
            await channel.send(line)
            in_event.append(author)

            a = await channel.send("請輸入要找的網址名子")
            pending[f'{author}'].append(client.wait_for('message', check=_check))
            site_url = await pending[f'{author}'][0]
            await site_url.delete()
            await add_reactions(a, "✅")

            b = await channel.send("請輸入密碼(ONLY NUMBERS)")
            pending[f'{author}'].append(client.wait_for('message', check=_check))
            master_pass = await pending[f'{author}'][1]
            await master_pass.delete()
            if not is_number(master_pass):
                await add_reactions(b, "❌") 
                await channel.send("對不起僅限數字")
                await channel.send(line)
                end_session(message, 1)
                return

            await add_reactions(b, "✅")

            await channel.send("完成資料收集")
            await channel.send(line)
            encode = sqlh.read_pass(author,site_url.content)
            if encode == None :
                error = await channel.send('找不到這個名子所儲存的密碼')
                await add_reactions(error, "❌")
                end_session(message, 1)
                return 
            decoded_pass = edcode.decode(int(master_pass.content), encode)


            
            send_pass = await channel.send(str(decoded_pass)) 
            await asyncio.sleep(int(setting_data.find(author, 'delete_time'))) #wait for _ seconds and than delete
            await send_pass.delete() 
            in_event.pop(in_event.index(author))    




        elif message.content.startswith('#deletepass'):
            in_event.append(author)
            a = await channel.send("請輸入你想刪除的網站")
            site_url = await client.wait_for('message', check=_check)
            result = sqlh.delete_pass(author, site_url.content)
            await channel.send(result)
            in_event.pop(in_event.index(author))



        
        elif message.content.startswith('#listSettings'):
            await channel.send(setting_data.find(author, 'all'))



        elif message.content.startswith('#settingChange'):
            in_event.append(author)
            await channel.send('你想要換哪個選項')
            option = await client.wait_for('message', check=_check)
            await channel.send('你想要換成什麼值')
            content = await client.wait_for('message', check=_check)
            result = setting_data.replace(author, option.content, content.content)
            await channel.send(result)

            in_event.pop(in_event.index(author))
        else:
            pass


    except RuntimeError:
        print('session_end')
    # Excepted Error,for canceling the pending message
    except Exception as e:
        if author in in_event:
            in_event.pop(in_event.index(author))
        await message.channel.send('!!!對不起發生了未知的錯誤!!!')
        await message.channel.send(f'`Error : {e}`')
        print(e)
        print('UnException Error')





#keep_alive() must be in front of the client.run(), otherwise it won't run.
keep_alive()
client.run(os.getenv('TOKEN'))
