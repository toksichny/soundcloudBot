from flask import Flask, request
from threading import Thread
import time
import requests
import socket

app = Flask('')


@app.route('/')
def home():
  return "I'm alive"


def run():
  host = '0.0.0.0'
  port = 80
  app.run(host=host, port=port)
  ip_address = socket.gethostbyname(socket.gethostname())
  print(f"Server is running at http://{ip_address}:{port}")


def keep_alive():
  t = Thread(target=run)
  t.start()


# Run the keep_alive function to start the server and print the URL
if __name__ == "__main__":
  keep_alive()
