import os
from time import sleep
from belltower import RingingRoomTower
from tkinter import *
from wheatley.main import main
from threading import Thread
import sys
from random_quote_generator import get_quote
from random_quote_generator.get_joke import get_joke
import numpy as np
import psutil


root = Tk()
towerID = 821597346

"""
def myClick1():
    global towerID
    towerID = 821597346
    myLabel = Label(root, text = "Selected 821597346")
    myLabel.pack()



myLabel1 = Label(root, text="Connect to Chilham tower")

myButton1 = Button(root, text = "Chilham", command = myClick1)
myLabel1.pack()
myButton1.pack()
myLabel2 = Label(root, text="Connect to another tower\nRinging Room tower ID:")
myLabel2.pack()
e = Entry(root)
e.pack()

def myClick2():
    global towerID
    towerID = int(e.get())
    myLabel = Label(root, text = "Selected" + str(e.get()))
    myLabel.pack()
    
myButton2 = Button(root, text = "Connect to other tower", command = myClick2).pack()
myButton2 = Button(root, text="Confirm", command=root.destroy).pack()

def write(*message, end = "\n", sep = " "):
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    Console.insert(INSERT, text)

Console = Text(root)
Console.pack()

root.mainloop()
"""

tower = RingingRoomTower(towerID)
msg_user, step, method, command = "",-1,"",[]

# Register a function to be called when a chat message is posted
@tower.on_chat
def on_chat(user, message):
    print(f"{user} says '{message}'")
    global msg_user, step, method, command
    # If the message is 'hello' in any capitalisation, send 'Hello <user>'.
    # The first argument is the name to put next to the chat message
    if message.lower() == "hello" or message.lower() == "hi":
        tower.chat("RR ChatBot", f"Hello, {user}!")


    if message.lower() == "quote please" or message.lower() == "random quote please" or message.lower() == "please quote" or message.lower() == "please random quote":
        tower.chat("Narrator", "An old man emerges from the heavy mist:")
        sleep(2)
        tower.chat("Old Man", str(get_quote()))

    if message.lower() == "joke please" or message.lower() == "jokes please" or message.lower() == "please joke" or message.lower() == "please jokes":
        tower.chat("Narrator", "A programmer appears:")
        sleep(2)
        tower.chat("Programmer", str(get_joke()))

    if msg_user == str(f"{user}") and step == 6:
        if str(message.lower()) != "default":
            command.append("--handstroke-gap")
            command.append(str(f"{message}"))
        command.append("--method")
        command.append(str(method))
        tower.chat("RR ChatBot","Wheatley Running")
        with open("command.txt", 'w') as f:
            for i in range(0, len(command)):
                f.write(command[i])
                f.write("\n")
        import WheatleyExecute
        msg_user, method, command, step = "","",[],-1
        tower.chat("RR ChatBot","Done")


    if msg_user == str(f"{user}") and step == 5:
        if str(message.lower()) != "default":
            command.append("--single")
            command.append(str(f"{message}"))
        step = step + 1
        tower.chat("RR ChatBot","Handstroke Gap: default for default")


    if msg_user == str(f"{user}") and step == 4:
        if str(message.lower()) != "default":
            command.append("--bob")
            command.append(str(f"{message}"))
        step = step + 1
        tower.chat("RR ChatBot",'Override for what place notation(s) should be made when a `Single` is called. Type "default" for default.')

    if msg_user == str(f"{user}") and step == 3:
        if str(message.lower()) == "y" or str(message.lower()) == "yes":
            command.append("--keep-going")
        step = step + 1
        tower.chat("RR ChatBot",'Override for what place notation(s) should be made when a `Bob` is called. Type "default" for default.')
    

    if msg_user == str(f"{user}") and step == 2:
        if str(message.lower()) == "y" or str(message.lower()) == "yes":
            tower.chat("RR ChatBot","Keep constant rhythm? y/n")
            step = step + 1
        else:
            command.append("--method")
            command.append(str(method))
            tower.chat("RR ChatBot","Wheatley Running")
            with open("command.txt", 'w') as f:
                for i in range(0, len(command)):
                    f.write(command[i])
                    f.write("\n")
            import WheatleyExecute
            msg_user, method , command , step = "","",[], -1
            tower.chat("RR ChatBot","Done")



    if msg_user == str(f"{user}") and step == 1:
        if str(message.lower()) == "y" or str(message.lower()) == "yes":
            command.append("--stop-at-rounds")
            command.append("--use-up-down-in")
        tower.chat("RR ChatBot","More Options? y/n")
        step = step + 1


    if msg_user == str(f"{user}") and step == 0:
        method = f"{message}"
        command.append(str(towerID))
        tower.chat("RR ChatBot","good settings: y/n")
        step = step + 1

    if str(f"{user}")!="RR ChatBot":
        if message.lower() == "/w":
            msg_user = str(f"{user}")
            tower.chat("RR ChatBot","Enter Method:")
            step = 0
        if message.lower() == "/w stop":
            tower.chat("RR ChatBot", "Wheatly Stopped")
            msg_user, method, command, step = "","",[], -2
            with open("PID.txt", 'r') as f:
                PID = 0
                for line in f:
                    PID = line
            p = psutil.Process(int(PID))
            p.terminate()
        if message.lower() == "/w stop" and step == -2:
            msg_user, method, command, step = "","",[], -2

    
        
        

# The 'with' block makes sure that 'tower' has a chance to gracefully shut
# down the connection if the program crashes

with tower:
    # Wait until the tower is loaded
    tower.wait_loaded()
    # Go into an infinite loop.  It doesn't matter what the main thread does,
    # but if it leaves the `with` block then the Tower's connection will
    # close and become unusable
    while True:
        sleep(1000)
        #print("texxt")


