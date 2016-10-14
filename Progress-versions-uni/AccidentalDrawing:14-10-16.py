#setup
#A E S T H E T I C
#Importing modules
from tkinter import * #enables use of the Tkinter UI, responsible for drawing of objects and generation of GUI
import sys #needed for setrecursionlimit which prevents a crash (may not be needed)
import time #needed for restriction of refresh rate (may not be needed)
import math #needed for physics calculation
import random #for some more fun parts of the program.
#functions and variables		

#many of these variables can easily be locatlised.

sys.setrecursionlimit(100000000) #redundant
master = Tk() #master window

alphabet=[]
for alpha in range (65,91): alphabet.append(chr(alpha))  #something like that
systemname = "Gravitpy - System:" , alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],"-",random.randint(0,9),random.randint(0,9),random.randint(0,9)
master.wm_title(systemname)


w = Canvas(master, width=1000, height=1000,bg="black") #generate 1000x1000 canvas
w.pack() #packdat
currr = 0 #The row number in the 2d array "OBJECTS" that is avalible for use.
rad = [] #radius 
numberofplanets=0 #duh
objectxy = 0 #centre of circle x/y
object2xy =0 #centre of second objects x/y
xforce = 0
yforce = 0
planets = 0
list1 = 0
objectarray = []
xp = True
yp = True
drawtrail = False
#debug lines
#w.create_rectangle(0,0, 1000, 1000, fill="black")
w.create_line(0, 0, 1000, 1000,fill="red", dash=(4, 4))
w.create_line(0, 1000, 1000, 0, fill="red", dash=(4, 4))
for i in range(1,10):
    lfill = "red"
    if i == 5: lfill = "green"
    w.create_line(100*i,0,100*i,1000,fill=lfill, dash = (4,4))
    w.create_line(0,100*i,1000,100*i, fill=lfill, dash = (4,4))
#constants
G = 6.673 * 10 **-11
#2d arrays
OBJECTS = [["n" for x in range(6)] for y in range(10)]#(Y,X) #2d array for planet variables
DELTAXY = [["n" for x in range(2)] for y in range(10)]#(Y,X) #2d array for the deltax/y speed of objects
LASTPOS = [["n" for x in range(2)] for y in range(10)]#(Y,X) #2d array for last position of object (mostly for trail)
"""
Collums of OBJECTS:
0 = x1
1 = y1
2 = x2
3 = y2
4 = mass
5 = colour
"""
def drawobjects():
       #time.sleep(1)
       w.update()
       if currr > 1:
           for main in range(0,currr):
               print("-------------------------------LOOP 1------------------------------")
               list1 = (OBJECTS[main][0],OBJECTS[main][2],OBJECTS[main][1],OBJECTS[main][3])
               objectxy = (int(OBJECTS[main][2] + 0.5*(int(OBJECTS[main][0]) - int(OBJECTS[main][2]))),(int(OBJECTS[main][3] + 0.5*(int(OBJECTS[main][1]) - int(OBJECTS[main][3])))))
               LASTPOS [main] = objectxy
               calculatedeltaXY(currr,G,DELTAXY,objectxy,object2xy,list1,main)
           moveobjects()
def moveobjects(): 
    global drawtrail
    for travel in range(0,currr):
        print("---------------------------------LOOP 3----------------------------------")
        print("currr",currr,"travel",travel)
        for ob in DELTAXY:
            print(ob)
        changex = DELTAXY[travel][0]
        changey = DELTAXY[travel][1]
        print("BEFORE",OBJECTS[travel][0],OBJECTS[travel][1],OBJECTS[travel][2],OBJECTS[travel][3])
        OBJECTS[travel][0] += int(changex)/1000000
        OBJECTS[travel][1] += int(changey)/1000000
        OBJECTS[travel][2] += int(changex)/1000000
        OBJECTS[travel][3] += int(changey)/1000000
        print("AFTER",OBJECTS[travel][0],OBJECTS[travel][1],OBJECTS[travel][2],OBJECTS[travel][3])
        w.update()
        w.delete("oval")
        for x in range(0,currr):
            for lmao in OBJECTS:
                print(lmao)
            print("currr",currr,"x",x)
            print(OBJECTS[x][0],OBJECTS[x][1],OBJECTS[x][2],OBJECTS[x][3],OBJECTS[x][4],OBJECTS[x][5])
            w.create_oval(OBJECTS[x][0],OBJECTS[x][1],OBJECTS[x][2],OBJECTS[x][3],fill=OBJECTS[x][5],tag="oval")
    travel = 0
def calculatedeltaXY(currr,G,DELTAXY,objectxy,object2xy,list1,main):
        xforce = 0
        yforce = 0
        planets = 0
        for planets in range(0,currr):
            object2xy = (int(OBJECTS[planets][2] + 0.5*(int(OBJECTS[planets][0]) - int(OBJECTS[planets][2])))),(int(OBJECTS[planets][3] + 0.5*(int(OBJECTS[planets][1]) - int(OBJECTS[planets][3]))))
            print("-------------------------------LOOP 2------------------------------")
            print("Planet 1",objectxy)
            print("Planet 2",object2xy)
            print("planets",planets,"numberofvalues",currr-1,"currr",currr)
            force = 0
            list2 = (OBJECTS[planets][0],OBJECTS[planets][2],OBJECTS[planets][1],OBJECTS[planets][3])
            if list1 == list2:
                print("Didn't consider duo",currr)
                continue      
            rad,theta,xp,yp = calculatevariables(objectxy,object2xy)
            if drawtrail == True:
                for i in LASTPOS:
                    print(i)
                if LASTPOS[planets][0] == "n": continue    
                w.create_line(objectxy[0],objectxy[1],LASTPOS[planets][0],LASTPOS[planets][1],fill="White",tags="trail")
                
            print("planetsinloop",planets)
            print(G,OBJECTS[currr-1][4],"obj",OBJECTS[planets][4],"rad",rad,"theta",theta)
            force = (((G*(OBJECTS[currr-1][4]*(10**24)))*(OBJECTS[planets][4]*(10**24)))/rad**2)
            #print("force",force, "theta",theta)
            xforce += ((force*math.sin(theta)) / (OBJECTS[currr-1][4]*(10**24)) / 10000)
            yforce += ((force*math.cos(theta)) / (OBJECTS[currr-1][4]*(10**24)) / 10000)
            if xp != False: xforce = -xforce
            if yp != False: yforce = -yforce
            print("xforce",xforce,"yforce",yforce)
        DELTAXY[main][0] = xforce
        DELTAXY[main][1] = yforce
def calculatevariables(objectxy,object2xy):
        #find radius between objects:
        global xp
        global yp
        xp = False
        yp = False
        a = objectxy[0] - object2xy[0]
        b = objectxy[1] - object2xy[1]
        print("a",a,"b",b)
        #Set difference in xy to a value that is used to calculate the radius and the angle
        if b == 0: b+=1 #if b=0 then the triangle looks like this: | therefore it must not be that as r would be divided by 0
        radius = math.sqrt((a**2) + (b**2))
        theta = math.degrees(round(math.atan(a/b)))
	#THIS FUNCTION NEEDS FIXING       
        if a > 0: yp = True
        if b > 0: xp = True
	#THISBIT
        return(radius,theta,xp,yp)
def clickfunct(event):
    global currr
    OBJECTS[currr][0] = event.x-3
    OBJECTS[currr][1] = event.y-3
    OBJECTS[currr][2] = event.x+3
    OBJECTS[currr][3] = event.y+3
    OBJECTS[currr][4] = 1
    OBJECTS[currr][5] = "White"
    w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill=OBJECTS[currr][5],tags="oval")
    currr +=1
def rclickfunct(event):
    #print(event.x,event.y)
    global currr
    OBJECTS[currr][0] = event.x-10
    OBJECTS[currr][1] = event.y-10
    OBJECTS[currr][2] = event.x+10
    OBJECTS[currr][3] = event.y+10
    OBJECTS[currr][4] = 10
    OBJECTS[currr][5] = "Yellow"
    w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill=OBJECTS[currr][5],tags="oval")
    currr +=1
def trailfunct(event):
    global drawtrail
    if drawtrail == True:
        w.delete("trail")
    drawtrail = not drawtrail

def delf(event):
    print(event)
    global OBJECTS
    global DELTAXY
    w.delete("trail","oval")
    print("okay")
    OBJECTS = [["n" for x in range(6)] for y in range(10)]#(Y,X) #2d array for planet variables
    DELTAXY = [["n" for x in range(2)] for y in range(10)]#(Y,X) #2d array for the deltax/y speed of objects

#keybinds
w.bind("<Button-1>",clickfunct)
w.bind("<Button-3>",rclickfunct)
w.bind("<Button-2>",trailfunct)
w.bind("<D>",delf)
while True: drawobjects()
