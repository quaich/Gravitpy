#setup
from tkinter import *
import sys
import time
import math
import random
sys.setrecursionlimit(100000000)
master = Tk()
master.wm_title("Gravitpy")
w = Canvas(master, width=1000, height=1000)
w.pack()
currr = 0
rad = []
numberofplanets=0
#debug lines
w.create_rectangle(0,0, 1000, 1000, fill="black")
w.create_line(0, 0, 1000, 1000,fill="red", dash=(4, 4))
w.create_line(0, 1000, 1000, 0, fill="red", dash=(4, 4))
for i in range(1,10):
    lfill = "red"
    if i == 5: lfill = "green"
    w.create_line(100*i,0,100*i,1000,fill=lfill, dash = (4,4))
    w.create_line(0,100*i,1000,100*i, fill=lfill, dash = (4,4))
#constants
G = 6.67300 * 10 **-11
#2d arrays
OBJECTS = [["n" for x in range(7)] for y in range(20)]#(Y,X)
DELTAXY = [["n" for x in range(2)] for y in range(20)]#(Y,X)
"""
Collums:
0 = x1
1 = x2
2 = y1
3 = y2
4 = mass
5 = dx
6 = dy
"""
done = False
clicked = False
sclicked = False
def drawobjects():
       done = False
       w.update()
       time.sleep(0.1)
       for i in range(0,20):
           if OBJECTS[i][0] == "n" and done != True:
               global currr
               currr = i
               done = True
       if sclicked == True:
           calculatedeltaXY()
       for i in range(0,20): DELTAXY[i] = ["n","n"]
       drawobjects()
def calculatedeltaXY():
        global currr
        global G
        global DELTAXY
        global objectxy
        global object2xy
        xforce = 0
        yforce = 0
        planets = 0
        objectxy = int(OBJECTS[currr-1][0]) - int(OBJECTS[currr-1][1]),int(OBJECTS[currr-1][2]) - int(OBJECTS[currr-1][3])
        list = (OBJECTS[currr-1][0],OBJECTS[currr-1][1],OBJECTS[currr-1][2],OBJECTS[currr-1][3])
        for planets in range(0,currr-1):
            print(planets)
            if OBJECTS[planets][0] != "n":
                print("=================================")
                print("planets",planets,"\r","numberofvalues",currr-1,"\r","currr",currr)
                print("=================================")
                force = 0
                object2xy = int(OBJECTS[planets][0]) - int(OBJECTS[planets][1]),int(OBJECTS[planets][2]) - int(OBJECTS[planets][3])
                list2 = (OBJECTS[planets][0],OBJECTS[planets][1],OBJECTS[planets][2],OBJECTS[planets][3])
              #  if list == list2:
             #       if OBJECTS[planets+1][0] != "n":
             #           planets +=1
              #  else:continue
                rad = calculateradius(objectxy,object2xy)
                dx = abs(objectxy[1] - object2xy[1])
                dy = abs(objectxy[0] - object2xy[0])
                if dx == 0: dx +=1
                theta = math.degrees(math.atan(dy//dx))
                print("planetsinloop",planets)
                print(G,OBJECTS[currr-1][4],"obj",OBJECTS[planets][4],"rad",rad)
                force = (G*(OBJECTS[currr-1][4]*10**24*OBJECTS[planets][4]*10**24)/rad**2)
                xforce += (force*math.sin(theta)) // (OBJECTS[currr-1][4]*10**24)/ 1000
                yforce += (force*math.cos(theta)) // (OBJECTS[currr-1][4]*10**24) / 1000
                print("xforce",xforce,"yforce",yforce)
            DELTAXY[currr-2][0] = xforce
            #DELTAXY[planets+1][0] += -xforce
            DELTAXY[currr-2][1] = yforce
            #DELTAXY[planets+1][1] += -yforce
            for each in DELTAXY:
                print(each)
def calculateradius(object1,object2):
        #find radius between objects:
        a = abs(objectxy[0] - object2xy[0])
        b = abs(objectxy[1] - object2xy[1])
        radius = math.sqrt(a** 2+ b** 2)
        return(radius)
def clickfunct(event):
    global clicked
    if clicked == True:
        global sclicked
        sclicked = True
    clicked = True
    print(event.x,event.y)
    global currr
    print("it is",clicked)
    print("INCLICK",currr)
    OBJECTS[currr][0] = event.x-3
    OBJECTS[currr][1] = event.y-3
    OBJECTS[currr][2] = event.x+3
    OBJECTS[currr][3] = event.y+3
    OBJECTS[currr][4] = 1
    OBJECTS[currr][5] = 0
    OBJECTS[currr][6] = 0
    w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill="white")
def rclickfunct(event):
    print(event.x,event.y)
    global clicked
    if clicked == True:
        global sclicked
        sclicked = True
    clicked = True
    OBJECTS[currr][0] = event.x-10
    OBJECTS[currr][1] = event.y-10
    OBJECTS[currr][2] = event.x+10
    OBJECTS[currr][3] = event.y+10
    OBJECTS[currr][4] = 10
    OBJECTS[currr][5] = 0
    OBJECTS[currr][6] = 0
    w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill="Yellow")
w.bind("<Button-1>",clickfunct)
w.bind("<Button-3>",rclickfunct)
complete = False
drawobjects()
