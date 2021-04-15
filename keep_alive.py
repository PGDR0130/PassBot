#source from https://gist.github.com/beaucarnes/51ec37412ab181a2e3fd320ee474b671
#using uptime robot to ping the sever so that it would run for ever and won't be down 

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()