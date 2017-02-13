#TODO

#2. Code spring cleaning.
#3. Remake UI
#4. Optimize and remove (as many as possible) globals




#setup
#Importing modules
from tkinter import * #enables use of the Tkinter UI, responsible for drawing of objects and generation of GUI
from tkinter import filedialog #Cannot run without this unless in IDLE
from tkinter.colorchooser import *
import time #needed for restriction of refresh rate (may not be needed)
import math #needed for physics calculation
import random #for some more fun parts of the program.
import datetime #for delta time calculations
#functions and variables
#many of these variables can easily be locatlised.
master = Tk() #master window
alphabet=[]
w = Canvas(master, width=1200, height=1000) #generate 1200x1000 canvas
master.resizable(width=False,height=False)
w.pack() #packdat
try: master.iconbitmap("icon.ico")
except: print("Icon not found. Continuing..")
speed = 1
tbp = False
tbpc = False
trail = False
starttime = time.time()
lasttime = starttime
paused = False
prevpaused = False
planetcolour = ((255,0,0),"#FF0000")
planetselected = 0

poplist = []
#constants
G = 6.6742 #simplfied
#2d arrays
OBJECTS = []#(Y,X) #2d array for planet variables

""" This is the worst way of doing this. I know OOP is a thing but that doesn't matter right now
Collums of OBJECTS:
0 = The x0
1 = The y0
2 = The x1
3 = The y1
4 = The mass
5 = The colour string
6 = The objects DELTAX
7 = The objects DELTAY
8 = LASTPOSX
9 = LASTPOSy
10 = radius of the object
11 = R
12 = G
13 = B
14 = Physical representation of the Planet on the plane
15 = time alive
16 = theta
17 = number of planets devoured
"""

def main():
       if len(OBJECTS) > 1:
               for mainl in range(0,len(OBJECTS)): #for more than one object

                       x = 0
                       alone = True
                       for lines in OBJECTS:
                           if lines[0] != "n":
                                if mainl != x:
                                    alone = False
                                    break
                           x+=1
                       if alone == True: solo(trail,planetcolour)
                       objectxy = [((OBJECTS[mainl][0]+OBJECTS[mainl][2])/2),((OBJECTS[mainl][1]+OBJECTS[mainl][3])/2)]
                       calculatedeltaXY(G,objectxy,mainl,OBJECTS,speed)
                       OBJECTS[mainl][8] = objectxy [0]
                       OBJECTS[mainl][9] = objectxy [1]
       if len(OBJECTS) == 1:
              for x in range(len(OBJECTS)): pass ##print(OBJECTS[x])
              solo(trail,planetcolour)
def solo(ntrail,planetcolour):
        x = ((OBJECTS[0][0]+OBJECTS[0][2])/2)
        y = ((OBJECTS[0][1]+OBJECTS[0][3])/2)
        w.move(OBJECTS[0][14],OBJECTS[0][6],OBJECTS[0][7])
        OBJECTS[0][0],OBJECTS[0][1],OBJECTS[0][2],OBJECTS[0][3] = w.coords(OBJECTS[0][14])
        nx = ((OBJECTS[0][0]+OBJECTS[0][2])/2)
        ny = ((OBJECTS[0][1]+OBJECTS[0][3])/2)
        xy = [x,y]
        nxy = [nx,ny]
        if trail == True: drawtrail(xy,nxy,0,trail,planetcolour)

def calculatedeltaXY(G,objectxy,mainl,OBJECTS,speed):
        for planets in range(0,len(OBJECTS)-1):

            if planets != mainl:
                object2xy = [((OBJECTS[planets][0]+OBJECTS[planets][2])/2),((OBJECTS[planets][1]+OBJECTS[planets][3])/2)]
                if object2xy != objectxy:
                           ###Essentialy the collision detection###
                           radius,theta,xn,yn = maths(objectxy,object2xy)
                           if colide(mainl,planets,radius) == True:
                                  if OBJECTS[mainl][10] >= OBJECTS[planets][10]:
                                         tbd = planets
                                         OBJECTS[mainl][4] += OBJECTS[planets][4]
                                         OBJECTS[mainl][17] += 1
                                  else:
                                         tbd = mainl
                                         OBJECTS[planets][4] += OBJECTS[mainl][4]
                                         OBJECTS[planets][17] += 1
                                  w.delete(OBJECTS[tbd][14])
                                  global poplist
                                  if tbd not in poplist:
                                      poplist.append(tbd)
                                  break
                           Euler(objectxy,object2xy,mainl,planets,OBJECTS,speed)

def maths(objectxy,object2xy):
        a = int(objectxy[0] - object2xy[0])
        b = int(objectxy[1] - object2xy[1])
        xn = False
        yn = False
        radius = math.sqrt((a**2) + (b**2)) #Pythagorus theorem
        if radius != 0:
               if a == 0 : theta = 0 #change in x is 0 and we dont want an error to be thrown.
               else: theta = abs(math.atan(b/a))
        else: theta = 0
        if radius == 0:
               radius = 1
        if b > 0: yn = True
        else: yn = False
        if a > 0: xn = True
        else: xn = False
        return(radius,theta,xn,yn)

def physics(mainl,planets,objectxy,object2xy,OBJECTS,speed):
       radius,theta,xn,yn = maths(objectxy,object2xy)
       if radius == 0: pass #no div by 0
       Fgrav = ((G*(int(OBJECTS[mainl][4])*(int(OBJECTS[planets][4]))))/radius**2) / OBJECTS[mainl][4]
       if xn == True:accelerationx = -(Fgrav*math.cos(theta))
       else:accelerationx = Fgrav*math.cos(theta)
       if yn == True: accelerationy = -(Fgrav*math.sin(theta))
       else: accelerationy = Fgrav*math.sin(theta)
       cspeed = (speed.get()/1000)
       #Resolving (Right) (positive x)
       vx = accelerationx*cspeed
       vy = accelerationy*cspeed
       #Resolving (Down) (positive y)
       return(vx,vy)

def Euler(objectxy,object2xy,mainl,planets,OBJECTS,speed):
       prevxy = objectxy
       vx,vy = physics(mainl,planets,objectxy,object2xy,OBJECTS,speed)
       OBJECTS[mainl][6] += vx
       OBJECTS[mainl][7] += vy


def createplanet(rad,mass,x,y,R,G,B,cx,cy,theta):
    global planetcolour
    OBJECTS.append(([x-rad,y-rad,x+rad,y+rad,mass,('#%02x%02x%02x' % (int(R//1), int(G//1), int(B//1))),cx,cy,x,y,rad,R,G,B,0,time.time(),theta,0]))
    OBJECTS[len(OBJECTS)-1][14] = w.create_oval(OBJECTS[len(OBJECTS) -1][0],OBJECTS[len(OBJECTS) -1][1],OBJECTS[len(OBJECTS) -1][2],OBJECTS[len(OBJECTS) -1][3],fill=(OBJECTS[len(OBJECTS) -1][5]),tags="oval")
    w.lower("oval")
    w.lower("star")

def colide(mainl,planets,radius):
    if radius < OBJECTS[mainl][10]:
        w.lower(OBJECTS[planets][14])
        if radius < OBJECTS[mainl][10]: return True
    elif radius < OBJECTS[planets][10]:
        w.lower(OBJECTS[mainl][14])
        if radius < OBJECTS[planets][10]: return True
    else: return False

###UI Related subroutines###

def trailtoggle():
    global trail
    if trailbutton["text"] == "Toggle Trail on": trailbutton["text"] = "Toggle Trail off"
    else: trailbutton["text"] = "Toggle Trail on"
    trail = not trail


def drawtrail(prevxy,objectxy,mainl,trail,planetcolour):
       global trailduration
       if trail == True:
           colour = planetcolour [1]
           trail = w.create_line(prevxy[0],prevxy[1],objectxy[0],objectxy[1],fill=OBJECTS[mainl][5],tags="t")
           w.lower(trail)
           if trailduration.get() != 0: master.after(int((trailduration.get())*1000),lambda:w.delete(trail))

def playpause(colourc):
       global paused
       if colourc == True:
           if paused != True:
                  prevpaused = paused
                  playp["text"] = " ► "
                  paused = True
       elif colourc ==  False:
           if playp["text"] == "▐▐  ": playp["text"] = " ► "
           else: playp["text"] = "▐▐  "
           paused = not paused
       w.update()

def safetypause(colourc):
       global tbp
       if paused == True:
              playpause(colourc)
              tbp = False
       else: tbp = True

def clickfunct(event):
       global ox
       global oy
       global mass
       global density
       global planetcolour
       nmass = int(mass.get())
       ndensity = int(density.get())
       if event.x < 1000:
              ox = event.x
              oy = event.y
              w.create_oval(event.x+(nmass/ndensity),event.y+(nmass/ndensity),event.x-(nmass/ndensity),event.y-(nmass/ndensity),fill=planetcolour[1],tags="shotoval")

def motion(event):
       w.delete("shot")
       global planetcolour
       colour = planetcolour[1]
       if event.x < 1000:
              w.create_line(ox,oy,event.x,event.y,fill=colour,tags="shot")

def release(event):
    if event.x < 1000:
       global planetcolour
       x = event.x
       y = event.y
       cx = event.x - ox
       cy = event.y - oy
       w.delete("shot")
       lmass = int(mass.get())
       ldensity = int(density.get())
       if lmass < ldensity: lmass = ldensity *2
       radius = lmass / ldensity
       end = [x,y]
       start = [ox,oy]
       rad,theta,xneg,yneg= maths(start,end)
       vx = cx/((lmass)*5)
       vy = cy/((lmass)*5)
       createplanet(round(radius),lmass,ox,oy,planetcolour[0][0],planetcolour[0][1],planetcolour[0][2],vx,vy,theta)
    w.delete("shotoval")

def getcolour(prevpaused):
    global paused
    global planetcolour
    global tbpc
    prevpaused = paused
    if paused == True:
           askcolour(prevpaused)
           tbpc = False
    else: tbpc = True

def askcolour(prevpaused):
       global planetcolour
       planetcolour = askcolor()

def startoggle(): #make these shift all in one direction at some point
    if stary["text"] == "Toggle Stars off":
        w.delete("star")
        stary["text"] = "Toggle Stars on"
    else:
        for i in range(0,1000):
            for x in range(0,1): #make this variable
                ran = random.randint(0,1000)
                w.create_oval(ran,i,ran,i,outline="White",tags="star")
        w.lower("star")
        stary["text"] = "Toggle Stars off"

###LOAD AND SAVE SYSTEM###
def load():
    #variables to be edited#
    global OBJECTS
    file = filedialog.askopenfilename(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to load")
    try:
       with open(file,'r') as load:
             temparray = []
             ##Reset Variables##
             systemname = ("PYxis - System: {}".format(file))
             master.wm_title(systemname)
             w.delete("t")
             ###Delete array###
             del OBJECTS[:]
             ###set array to the file###
             lines = [line.split() for line in load]
             for line in range(0,len(lines)):
                    temparray.append(lines[line])

             w.delete("oval")
             ###convert to float###
             for y in range(0,len(temparray)):
                     for x in range(len(temparray[y])):
                            try: temparray[y][x] = float(temparray[y][x])
                            except: pass
       for lines in range(0,len(temparray)):
            createplanet(temparray[lines][10],temparray[lines][4],((temparray[lines][0]+temparray[lines][2])/2),((temparray[lines][1]+temparray[lines][3])/2),temparray[lines][11],temparray[lines][12],temparray[lines][13],temparray[lines][6],temparray[lines][7],0)
    except FileNotFoundError:
              print("No file was found.")
    dumpobjects()

def popplanets(): 
    global OBJECTS
    global poplist
    for planet in range(len(poplist)):
        print("Destroying planet:",poplist[planet])
        w.delete(OBJECTS[poplist[planet]][14])
        OBJECTS.pop(poplist[planet])
    poplist = []

def save():
    file = filedialog.asksaveasfile(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to save",defaultextension=".gpy")
    end = False
    for lines in OBJECTS:
              if lines[0] == "d": continue
              if end != True:
                     for entity in lines:
                            if lines[0] == "n":
                                   end = True
                                   file.write(str(entity))
                                   break
                            file.write(str(entity))
                            file.write(" ")
                     file.write("\n")
              else: break
    file.close()

def selectobject(event):
       x = event.x
       y = event.y
       closest = w.find_closest(x,y)
       try:
              if w.gettags(closest)[0] == "oval":
                     coords = w.coords(closest)
                     for i in range(0,len(OBJECTS) -1):
                            if coords == [OBJECTS[i][0],OBJECTS[i][1],OBJECTS[i][2],OBJECTS[i][3]]:
                                         global planetselected
                                         planetselected = i
              else: print("There's no planets around here!")
       except: pass
def deltrail():
       w.delete("t")

def dumpobjects():
       global OBJECTS
       for x in range(0,len(OBJECTS)):
              print(OBJECTS[x])



#------------------------------------------UI SECTION------------------------------------------#
w.configure(background="Black")
b1 = w.create_rectangle(1001,0,1205,1000,fill="white")

playp = Button(master,text="▐▐  ", command =lambda:safetypause(False),font=("Helvetica", 12))
playp.place(x=1150,y=5,width=30,height=30)

trailbutton = Button(master, text="Toggle Trail on", command=trailtoggle)
trailbutton.place(x=1040,y=120,width=120)

colourchoose = Button(master,text="Select colour",command=lambda:getcolour(prevpaused))
colourchoose.place(x=1040,y=300,width = 120)

deltrailb = Button(master,text="Delete Trails",command=deltrail)
deltrailb.place(x=1100,y=60,width=80)

loadfunct = Button(master,text="Load file",command=load)
loadfunct.place(x=1060,y=415,width=80)

savefunct = Button(master,text="Save file",command=save)
savefunct.place(x=1060,y=385,width=80)

stary = Button(master, text="Toggle Stars on", command=startoggle)
stary.place(x=1040,y=150,width=120)

curtime = w.create_text(50,30,fill = "White")
fps =     w.create_text(150,30,fill = "White")

###Planet specific variables###

w.create_rectangle(1020,90,1180,190,fill="Light Grey")
w.create_rectangle(1020,200,1180,340,fill="Light Grey")
w.create_rectangle(1020,350,1180,450,fill="Light Grey")
w.create_rectangle(1001,460,1250,470,fill="BLACK")
w.create_rectangle(1020,480,1180,660,fill="Light Grey")
w.create_text(1100,105,text="Toggle Functions",font=("Helvetica",10,"bold underline"))
w.create_text(1100,366,text="Load and save",font=("Helvetica",10,"bold underline"))
w.create_text(1100,215,text="Planet Properties",font=("Helvetica",10,"bold underline"))

#Mass#

mass = IntVar()
mass.set(100)
w.create_text(1060,247,text= "Mass",font=("Helvetica", 10))
Mass = Entry(master,width=10,textvariable=mass)
Mass.place(x=1100,y=240)

#Density#

density = IntVar()
density.set(20)
w.create_text(1065,277,text= "Density",font=("Helvetica",10))
Density = Entry(master,width=10, textvariable=density)
Density.place(x=1100,y = 270)

#Trail Duration#

trailduration = IntVar()
trailduration.set(0)
w.create_text(1100,687,text="Trail duration\n(0 = forever)",font=("Helvetica",10))
trailduration = Scale(master,from_=0,to=20,orient=HORIZONTAL)
trailduration.place(x=1050,y=710)
#Planet variable showing#

w.create_text(1100,495,text="Planet Information",font=("Helvetica",10,"bold underline"))

w.create_text(1062,520,text="Velocity")
planetvelocity = IntVar()
showoffvelocity = Entry(master,width=6,textvariable=planetvelocity)
showoffvelocity.place(x=1100,y=513)
planetvelocity.set(0)
showoffvelocity.configure(state="disabled")

w.create_text(1062,550,text="Mass")
planetmass = IntVar()
showoffmass = Entry(master,width=6,textvariable=planetmass)
showoffmass.place(x=1100,y=540)
planetmass.set(0)
showoffmass.configure(state="disabled")

w.create_text(1062,572,text="Density")
planetdensity = IntVar()
showoffdensity = Entry(master,width=6,textvariable=planetdensity)
showoffdensity.place(x=1100,y=567)
planetdensity.set(0)
showoffdensity.configure(state="disabled")

w.create_text(1062,605,text="Devorered\n  planets")
planetsdevoured = IntVar()
showoffdevoured = Entry(master,width=6,textvariable=planetsdevoured)
showoffdevoured.place(x=1100,y=595)
planetsdevoured.set(0)
showoffdevoured.configure(state="disabled")

w.create_text(1062,635,text="Time alive(s)")
planetalivetime = IntVar()
showoffalive = Entry(master,width=6,textvariable=planetalivetime)
showoffalive.place(x=1100,y=625)
planetalivetime.set(0)
showoffalive.configure(state="disabled")

w.create_text(1035,20,text="Force amp")
speed = Scale(master,from_=1,to=100,resolution=1,variable=speed,orient=HORIZONTAL,bg="white",length = 50,width=20)
speed.place(x=1085,y=5)

###    TITLE    ###

for alpha in range (65,91): alphabet.append(chr(alpha))  #something like that
systemname = ("PYxis - System: {}{}-{}{}{}".format(alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],random.randint(0,9),random.randint(0,9),random.randint(0,9))) #Standard string consentraition methods leave ugly curly brackets.
master.wm_title(systemname)

##Startoggle##
startoggle()
#------------------------------------------UI SECTION END--------------------------------------#
#keybinds
w.bind("<Button-1>",clickfunct) #initial click
w.bind("<B1-Motion>",motion) #click and drag
w.bind("<ButtonRelease-1>",release) #release of click
w.bind("<Button-3>",selectobject)


while True:
    if paused != True:
           w.itemconfig(curtime,text=("Time",round(time.time() - starttime,2)))
           otime = time.time()
           popplanets()
           main()
           try: w.itemconfig(fps,text=("FPS:", round(1/(time.time()-otime))))
           except ZeroDivisionError: pass #if the time change is too low

           ##Pause safely##
           if tbp == True or tbpc == True:
                  if tbpc == True:
                         playpause(True)
                         askcolour(prevpaused)
                         playpause(False)
                         tbpc = False
                  else: playpause(False)
           ##Selected planet attributes##
           if len(OBJECTS) -1 > 0:
                  planetvelocity.set(math.sqrt(((OBJECTS[planetselected][6])**2) +  ((OBJECTS[planetselected][7])**2))*100)
                  planetmass.set(OBJECTS[planetselected][4])
                  planetdensity.set(OBJECTS[planetselected][4] / OBJECTS[planetselected][10])
                  planetalivetime.set(round(time.time() - OBJECTS[planetselected][15]))
                  planetsdevoured.set(OBJECTS[planetselected][17])
            ##Move the planets in time with the rest of the program.##
           #I decided not to function this to save on calling globals##
           for number in range(0,len(OBJECTS)):
                  if OBJECTS[number][0] != "n":
                     w.move(OBJECTS[number][14],OBJECTS[number][6],OBJECTS[number][7])
                     oldxy = [((OBJECTS[number][0]+OBJECTS[number][2])/2),((OBJECTS[number][1]+OBJECTS[number][3])/2)]
                     try: OBJECTS[number][0],OBJECTS[number][1],OBJECTS[number][2],OBJECTS[number][3] = w.coords(OBJECTS[number][14])
                     except ValueError: pass
                     newxy = [((OBJECTS[number][0]+OBJECTS[number][2])/2),((OBJECTS[number][1]+OBJECTS[number][3])/2)]
                     if trail==True: drawtrail(oldxy,newxy,number,trail,planetcolour)
    w.update()
