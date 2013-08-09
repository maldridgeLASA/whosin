import jsondb
import RFID
import sys
import logging

import settings


door="testDoor"

def init():
    global keydb
    global doordb
    global connection
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Welcome to 'whosin'".center(80, '-'))
    keydb = jsondb.db("keys.db")
    doordb = jsondb.db("doors.db")
    reader = RFID.RFIDReader(settings.portName, settings.baudRate)

def auth(key, door):
    if keydb.lookup[key]["auth"] < door.db.lookup[door]["auth"]:
        return True
    else:
        return False

def openDoor(door):
    print "Opening door: {0}".format(door)

def main():
    while True:
        key = reader.read() #in production, the ID microprocessor would need to also return the door that originated the scan
        if auth(key, door):
            openDoor(door)
        else:
            print "Not Authorized"
