# Discord密碼機器人製作 - Passbot
`109-2 高一下自主學習`    竹北高中 11311 張哲誠

用Discord API + Pyhton做出一個密碼的機器人-->Passbot


***


* [Youtube 成品]( https://youtu.be/3t7k3uaSm8I )

* [準備檔案](https://drive.google.com/drive/folders/1vSz8nacTxxIkSUmdMed60ukV4vNs0VxC?usp=sharing)

**作品簡述:**

一個可以管理密碼的機器人，在不同的裝置使用，並且所有的密碼都加密儲存在雲端。  


使用Repl.it線上編譯器當作Discord機器人的伺服器，使用UptimeRobot讓編譯器不休眠、

用SQLite儲存加密後的資料、Json儲存使用者設定。



***




### Passbot 指令



>  **密碼**
> 
> > `#addpass` - 增加新的密碼到資料庫
> > 
> > `#findpass` - 拿取資料庫裡儲存的密碼
> > 
> > `#deletepass` - 刪除密碼
> > 
> > `#passlist` - 列出所有儲存的密碼
> 
>  **設定**
> > 
> > `#listSettings` - 列出所有設定
> > 
> > `#settingChange` - 更改設定
> > 
>  特殊
> > `#end_session` - 可以在發生錯誤或終止#addpass、#findpass使用





### 參考資料

> [Code a Discord Bot with Python](https://youtu.be/SPTfmiYiuok) - Youtube, By.Beau Carnes
> 
> [Python Asynchronous Programming](https://youtu.be/t5Bo1Je9EmE) - Youtube, By.Tech With Tim
> 
> [Discord API Doc](https://discordpy.readthedocs.io/en/stable/api.html)
> 
> [Cancel pending](https://stackoverflow.com/questions/57673106/how-to-cancel-a-pending-wait-for) - stackoverflow questions


### 使用的套件
> [discord.py](https://pypi.org/project/discord.py/) - Discord API 套件
> 
> [異步套件(asyncio)](https://pypi.org/project/asyncio/)
> 
> [pysqlite3](https://pypi.org/project/pysqlite3/) - sqlite3 資料庫套件



### 程式碼
> [完整程式碼]( https://github.com/PGDR0130/passbot )
>> [加密器程式碼](https://github.com/PGDR0130/passbot/blob/master/edcode.py) (edcode.py)
>> 
>> [SQLite 讀寫](https://github.com/PGDR0130/passbot/blob/master/sql_handler.py) (sql_handler.py)
>> 
>> [JSON檔案讀寫](https://github.com/PGDR0130/passbot/blob/master/setRW.py) (setRW.py)
>> 
>> [Relp.it 建立網站](https://github.com/PGDR0130/passbot/blob/master/keep_alive.py) (keep_alive.py) - By.Beau Carnes
> 
> [異步協成範例](https://gist.github.com/PGDR0130/2caa30b19446236e5c26fc97e2904c99)



