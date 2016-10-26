#setup
#Importing modules
from tkinter import * #enables use of the Tkinter UI, responsible for drawing of objects and generation of GUI
import time #needed for restriction of refresh rate (may not be needed)
import math #needed for physics calculation
import random #for some more fun parts of the program.
#functions and variables		
#many of these variables can easily be locatlised.
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


step = 8 #Euler step amount


objectarray = []
xn = True
yn = True
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
OBJECTS = [["n" for x in range(10)] for y in range(10)]#(Y,X) #2d array for planet variables
"""
Collums of OBJECTS:
0 = x0
1 = y0
2 = x1
3 = y1
4 = mass
5 = colour
6 = DELTAX
7 = DELTAY
8 = LASTPOSX
9 = LASTPOSy
"""
def drawobjects():
       if currr > 1:
           for main in range(0,currr):
               for sno in range(0,step+1):
                   #print("-------------------------------LOOP 1------------------------------")
                   list1 = (OBJECTS[main][0],OBJECTS[main][1],OBJECTS[main][2],OBJECTS[main][3])
                   #objectxy = (OBJECTS[main][2] + 0.5*OBJECTS[main][0] - OBJECTS[main][2]),(round(OBJECTS[main][3] + 0.5*(round(OBJECTS[main][1]) - round(OBJECTS[main][3])))))
                   objectxy = ((OBJECTS[main][0]+OBJECTS[main][2])/2),((OBJECTS[main][1]+OBJECTS[main][3])/2)
                   OBJECTS[main][6] = objectxy [0]
                   OBJECTS[main][7] = objectxy [1]
                   calculatedeltaXY(currr,G,objectxy,object2xy,list1,main)
                   OBJECTS[main][8] = objectxy [0]
                   OBJECTS[main][9] = objectxy [1]
           moveobjects()
def moveobjects(): 
    global drawtrail
    for travel in range(0,currr):
        #print("---------------------------------LOOP 3----------------------------------")
        #print("currr",currr,"travel",travel)
        changex = OBJECTS[travel][6]
        changey = OBJECTS[travel][7]
        #print("BEFORE",OBJECTS[travel][0],OBJECTS[travel][1],OBJECTS[travel][2],OBJECTS[travel][3],changex,changey)        
        OBJECTS[travel][0] += (round(changex)/100000)
        OBJECTS[travel][1] += (round(changey)/100000)
        OBJECTS[travel][2] += (round(changex)/100000)
        OBJECTS[travel][3] += (round(changey)/100000)
        #print("AFTER",OBJECTS[travel][0],OBJECTS[travel][1],OBJECTS[travel][2],OBJECTS[travel][3])
        #objectxy = (round(OBJECTS[travel][2] + 0.5*(round(OBJECTS[travel][0]) - round(OBJECTS[travel][2]))),(round(OBJECTS[travel][3] + 0.5*(round(OBJECTS[travel][1]) - round(OBJECTS[travel][3])))))
        objectxy = ((OBJECTS[travel][0]+OBJECTS[travel][2])/2),((OBJECTS[travel][1]+OBJECTS[travel][3])/2)
        if drawtrail == True:
            if OBJECTS[travel][8] == "n": continue
            w.create_line(OBJECTS[travel][8],OBJECTS[travel][9],objectxy[0],objectxy[1],fill="white",tags="trail")
        w.update()
        w.delete("oval")
        for x in range(0,currr):
            #print("currr",currr,"x",x)
            w.create_oval(OBJECTS[x][0],OBJECTS[x][1],OBJECTS[x][2],OBJECTS[x][3],fill=OBJECTS[x][5],tag="oval")
def calculatedeltaXY(currr,G,objectxy,object2xy,list1,main):
        xforce = 0
        yforce = 0
        for planets in range(0,currr):
            #object2xy = (round((OBJECTS[planets][2]) + 0.5*(round((OBJECTS[planets][0])) - round(OBJECTS[planets][2])))),(round(OBJECTS[planets][3] + 0.5*(round(OBJECTS[planets][1]) - round(OBJECTS[planets][3]))))
            object2xy = ((OBJECTS[planets][0]+OBJECTS[planets][2])/2),((OBJECTS[planets][1]+OBJECTS[planets][3])/2)
            #print("-------------------------------LOOP 2------------------------------")
            #print("Planet 1",objectxy)
            #print("Planet 2",object2xy)
            #print("planets",planets,"numberofvalues",currr-1,"currr",currr)
            force = 0
            list2 = (OBJECTS[planets][0],OBJECTS[planets][1],OBJECTS[planets][2],OBJECTS[planets][3])
            #print("list1",list1,"list2",list2)
            if list1 == list2:
                #print("Didn't consider duo",currr)
                continue      
            rad,theta,xn,yn = calculatevariables(objectxy,object2xy)           
            #print("planetsinloop",planets)
            #print(G,OBJECTS[currr-1][4],"obj",OBJECTS[planets][4],"rad",rad,"theta",theta)
            force = ((G*OBJECTS[currr-1][4]*(10**24)*(OBJECTS[planets][4]*(10**24)))/rad**2)/8
            if xn == True: xforce += -((force*math.sin(theta)) / (OBJECTS[currr-1][4]*(10**24)) / 10000)
            else: xforce += ((force*math.sin(theta)) / (OBJECTS[currr-1][4]*(10**24)) / 10000)
            if yn == True: yforce += -((force*math.cos(theta)) / (OBJECTS[currr-1][4]*(10**24)) / 10000)
            else: yforce += ((force*math.cos(theta)) / (OBJECTS[currr-1][4]*(10**24)) / 10000)
            #print("xforce",xforce,"yforce",yforce)
        OBJECTS[main][6] = xforce
        OBJECTS[main][7] = yforce
def calculatevariables(objectxy,object2xy):
        #find radius between objects:
        global xn
        global yn
        xn = False
        yn = False
        #print(objectxy[0],objectxy[1])
        a = int(objectxy[0]) - int(object2xy[0])
        b = int(objectxy[1]) - int(object2xy[1])
        #print("a",a,"b",b)
        #Set difference in xy to a value that is used to calculate the radius and the angle
        #if b == 0: b+=1 #if b=0 then the triangle looks like this: | therefore it must not be that as r would be divided by 0
        radius = math.sqrt((a**2) + (b**2))
        if b == 0 : b +=1
        theta = abs(math.degrees(math.atan(round(a/b))))
        ##print("div",a/b,"atan",math.atan(a/b),"rounded div",round(a/b),"roundedatan",math.atan(round(a/b)))
        if a > 0: xn = True
        if b > 0: yn = True
        #print("xn",xn,"yn",yn)
        return(radius,theta,xn,yn)
def clickfunct(event):
    global currr
    OBJECTS[currr][0] = event.x-3
    OBJECTS[currr][1] = event.y-3
    OBJECTS[currr][2] = event.x+3
    OBJECTS[currr][3] = event.y+3
    OBJECTS[currr][4] = 0.1
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
    if drawtrail == True: w.delete("trail")
    drawtrail = not drawtrail
#keybinds
w.bind("<Button-1>",clickfunct)
w.bind("<Button-3>",rclickfunct)
w.bind("<Button-2>",trailfunct)
while True:
    drawobjects()
    w.update()
