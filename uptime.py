# THIS IS A SUPPORT FOR HOSTING A DISCORD BOT ON REPL.IT EVEN AFTER YOU CLOSE THE webpage
# DO NOT CHANGE OR DELETE ANYTHING FROM HERE
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
