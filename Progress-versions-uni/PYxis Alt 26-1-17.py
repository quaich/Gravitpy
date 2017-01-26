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
import platform #for os related code
#functions and variables
#many of these variables can easily be locatlised.
master = Tk() #master window
alphabet=[]
w = Canvas(master, width=master.winfo_screenwidth(), height=master.winfo_screenheight()) #generate fullscreen canvas
w.pack()
currrscale = 100
master.overrideredirect(True)
try: master.iconbitmap("icon.ico")
except: pass
currr = 0 #The row number in the 2d array "OBJECTS" that is avalible for use.
xforce = 0
yforce = 0
speed = 1
currr
trail = False
starttime = time.time()
lasttime = starttime
paused = False
prevpaused = False
imported = False
planetcolour = ((255,0,0),"#FF0000")
planetselected = 0
fullscreen = False
#constants
G = 6.6742 #2004 mesurement
#2d arrays
OBJECTS = [["n" for x in range(18)] for y in range(200)]#(Y,X) #2d array for planet variables
exclude = [] #temporary mesure
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
tbp = False
tbpc = False

def main():
       if currr > 1:
               for mainl in range(0,currr): #for more than one object
                   if mainl not in exclude:
                       x = 0
                       alone = True
                       for lines in OBJECTS:
                           if lines[0] != "n" and lines[0] != "d":
                                if mainl != x:
                                    alone = False
                                    break
                           x+=1
                       if alone == True: solo(mainl,trail,planetcolour)
                       if OBJECTS[mainl][0] != "n" and OBJECTS[mainl][0] != "d":
                           objectxy = [((OBJECTS[mainl][0]+OBJECTS[mainl][2])/2),((OBJECTS[mainl][1]+OBJECTS[mainl][3])/2)]
                           calculatedeltaXY(currr,G,objectxy,mainl,exclude,OBJECTS,speed)
                           OBJECTS[mainl][8] = objectxy [0]
                           OBJECTS[mainl][9] = objectxy [1]
       if currr == 1: solo(0,trail,planetcolour)

def solo(no,trail,planetcolour):
        x = ((OBJECTS[no][0]+OBJECTS[no][2])/2)
        y = ((OBJECTS[no][1]+OBJECTS[no][3])/2)
        w.move(OBJECTS[no][14],OBJECTS[no][6],OBJECTS[no][7])
        OBJECTS[no][0],OBJECTS[no][1],OBJECTS[no][2],OBJECTS[no][3] = w.coords(OBJECTS[no][14])
        nx = ((OBJECTS[no][0]+OBJECTS[no][2])/2)
        ny = ((OBJECTS[no][1]+OBJECTS[no][3])/2)
        xy = [x,y]
        nxy = [nx,ny]
        if trail == True: drawtrail(xy,nxy,no,trail,planetcolour)

def calculatedeltaXY(currr,G,objectxy,mainl,exclude,OBJECTS,speed):
        for planets in range(0,currr):
            if OBJECTS[planets][0] != "n" and OBJECTS[planets][0] != "d" and planets not in exclude:
                object2xy = [((OBJECTS[planets][0]+OBJECTS[planets][2])/2),((OBJECTS[planets][1]+OBJECTS[planets][3])/2)]
                if object2xy != objectxy:
                       ###Essentialy the collision detection###
                       if planets not in exclude and mainl not in exclude:
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

                                  exclude.append(tbd)
                                  w.delete(OBJECTS[tbd][14])
                                  for x in range(0,len(OBJECTS[tbd])): OBJECTS[tbd][x] = "d"
                                  continue
                           Euler(objectxy,object2xy,mainl,planets,exclude,OBJECTS,speed)

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

def physics(mainl,planets,objectxy,object2xy,exclude,OBJECTS,speed):
       global currrscale 
       radius,theta,xn,yn = maths(objectxy,object2xy)
       if radius == 0: pass #no div by 0
       Fgrav = (((G*(int(OBJECTS[mainl][4])*(int(OBJECTS[planets][4]))))/radius**2) / OBJECTS[mainl][4])*(currrscale/100)
       if xn == True:accelerationx = -(Fgrav*math.cos(theta))
       else:accelerationx = Fgrav*math.cos(theta)
       if yn == True: accelerationy = -(Fgrav*math.sin(theta))
       else: accelerationy = Fgrav*math.sin(theta)
       cspeed = (speed/1000)
       #Resolving (Right) (positive x)
       vx = accelerationx*cspeed
       vy = accelerationy*cspeed
       #Resolving (Down) (positive y)
       return(vx,vy)

def Euler(objectxy,object2xy,mainl,planets,exclude,OBJECTS,speed):
       prevxy = objectxy
       vx,vy = physics(mainl,planets,objectxy,object2xy,exclude,OBJECTS,speed)
       OBJECTS[mainl][6] += vx
       OBJECTS[mainl][7] += vy


def createplanet(rad,mass,x,y,R,G,B,cx,cy,theta):
    global planetcolour
    global currr
    rad = math.sqrt(rad)
    OBJECTS[currr][11],OBJECTS[currr][12],OBJECTS[currr][13] = R,G,B
    OBJECTS[currr] = [x-rad,y-rad,x+rad,y+rad,mass,'#%02x%02x%02x' % ((int(OBJECTS[currr][11]//1), int(OBJECTS[currr][12]//1), int(OBJECTS[currr][13]//1))),cx,cy,x,y,rad,R,G,B,0,time.time(),theta,0]
    OBJECTS[currr][14] = w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill=(OBJECTS[currr][5]),tags="oval")
    currr +=1
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
       ox = event.x
       oy = event.y
       w.create_oval(event.x+(math.sqrt(nmass/ndensity)),event.y+(math.sqrt(nmass/ndensity)),event.x-(math.sqrt(nmass/ndensity)),event.y-(math.sqrt(nmass/ndensity)),fill=planetcolour[1],tags="shotoval")

def motion(event):
       w.delete("shot")
       global planetcolour
       colour = planetcolour[1]
       global ox
       global oy
       w.create_line(ox,oy,event.x,event.y,fill=colour,tags="shot")

def release(event):
       global planetcolour
       global ox
       global oy
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
        w.delete("s")
        stary["text"] = "Toggle Stars on"
    else:
        for i in range(0,master.winfo_screenwidth()):
            for x in range(0,2): #make this variable
                ran = random.randint(0,master.winfo_screenwidth())
                w.create_oval(ran,i,ran,i,outline="White",tags="s")
        w.lower("s")
        stary["text"] = "Toggle Stars off"

###LOAD AND SAVE SYSTEM###
def load():
    #variables to be edited#
    global currr
    global imported
    global OBJECTS
    global exclude
    global currrscale
    file = filedialog.askopenfilename(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to load")
    try:
       with open(file,'r') as load:
             ##Reset Variables##
             systemname = ("PYxis - System: {}".format(file))
             master.wm_title(systemname)
             currr = 0
             imported = True
             exclude = []
             w.delete("t")
             ###Delete array###
             for dely in range(0,len(OBJECTS)):
                    for delx in range(0,len(OBJECTS[dely])):
                           OBJECTS[dely][delx] = "n"
             ###set array to the file###
             lines = [line.split() for line in load]
             for line in range(0,len(lines)):
                    if len(lines) < line:
                          OBJECTS[line] = ["n" for i in range(len(OBJECTS[1]))]
                    else: OBJECTS[line] = lines[line]
             w.delete("oval")
             ###convert to float###
             for y in range(0,len(OBJECTS)):
                     if OBJECTS[y][0] == "n": break
                     for x in range(0,18):
                            try: OBJECTS[y][x] = float(OBJECTS[y][x])
                            except: pass
       for lines in range(0,len(OBJECTS)):
            currr = lines
            if OBJECTS[lines][0] == "n": break
            if OBJECTS[lines][1] != "d":
                   OBJECTS[lines][6] =  OBJECTS[lines][6] * (currrscale/100)
                   OBJECTS[lines][7] = OBJECTS[lines][7] * (currrscale/100)
                   createplanet(OBJECTS[lines][10],OBJECTS[lines][4],((OBJECTS[lines][0]+OBJECTS[lines][2])/2),((OBJECTS[lines][1]+OBJECTS[lines][3])/2),OBJECTS[lines][11],OBJECTS[lines][12],OBJECTS[lines][13],OBJECTS[lines][6],OBJECTS[lines][7],0)
    except FileNotFoundError:
              print("No file was found.")

def save():
       file = filedialog.asksaveasfile(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to save",defaultextension=".gpy")
       for lines in OBJECTS:
              for entity in lines:
                     file.write(str(entity))
                     file.write(" ")
                     if lines[0] == "n": break
              file.write("\n")
       file.close()

def selectobject(event):
       x = event.x
       y = event.y
       closest = w.find_closest(x,y)
       try:
              if w.gettags(closest)[0] == "oval":
                     coords = w.coords(closest)
                     for i in range(0,currr):
                            if coords == [OBJECTS[i][0],OBJECTS[i][1],OBJECTS[i][2],OBJECTS[i][3]]:
                                         global planetselected
                                         planetselected = i
              else: print("There's no planets around here!")
       except: pass
def deltrail():
       w.delete("t")
def scroll(event): #account for both windows and linux systems.
       global currrscale
       if platform.system() == "Windows":
              if event.delta % 120 == 0 and event.delta > 0:
                     scale = 1.4285714285714286
              if event.delta % 120 == 0 and event.delta < 0:
                     scale = 0.7

       if platform.system() == "Linux":
              if event.num % 4 == 0 and event.num > 0:
                     scale = 1.4285714285714286
              if event.num % 5 == 0:
                     scale = 0.7
       try:
              if scale > 1 or currrscale > 100:
                     w.scale("s",event.x,event.y,scale,scale)
              else:
                     startoggle()
                     startoggle()

              w.scale("oval",event.x,event.y,scale,scale)
              w.scale("t",event.x,event.y,scale,scale)
              currrscale = currrscale * scale
       except: pass
       w.delete("t")
def dragstart(event):
       w.scan_mark(event.x,event.y)
def dragend(event):
       print(event.x,event.y)
       w.scan_dragto(event.x,event.y,gain=1)
def fullscreentoggle():
       global fullscreen
       fullscreen = not fullscreen
       master.overrideredirect(fullscreen)
#------------------------------------------UI SECTION------------------------------------------#
fullscreentoggle()
w.configure(background="Black")
playp = Button(master,text="▐▐  ", command =lambda:safetypause(False),font=("Helvetica", 12))
trailbutton = Button(master, text="Toggle Trail on", command=trailtoggle)
colourchoose = Button(master,text="Select colour",command=lambda:getcolour(prevpaused))
deltrailb = Button(master,text="Delete Trails",command=deltrail)
loadfunct = Button(master,text="Load file",command=load)
savefunct = Button(master,text="Save file",command=save)
stary = Button(master, text="Toggle Stars on", command=startoggle)
mass = IntVar()
mass.set(1000)
density = IntVar()
density.set(20)
trailduration = IntVar()
trailduration.set(0)
trailduration = Scale(master,from_=0,to=20,orient=HORIZONTAL)
trailduration.place(x=(master.winfo_screenwidth()-200),y=(master.winfo_screenheight()-100))
##Menus##

#File#
menubar = Menu(master)
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label="Open", command=load)
filemenu.add_command(label="Save as",command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=master.destroy)
menubar.add_cascade(label="File",menu=filemenu)
#Edit#
editmenu = Menu(menubar,tearoff=0)
editmenu.add_command(label="Colour",command=lambda:getcolour(prevpaused))
editmenu.add_command(label="Toggle Trail",command=trailtoggle)
editmenu.add_command(label="Toggle Stars", command=startoggle)
menubar.add_cascade(label="Edit",menu=editmenu)

#view#
viewmenu = Menu(menubar,tearoff=0)
viewmenu.add_command(label ="Fullscreen",command=fullscreentoggle)
menubar.add_cascade(label="View",menu=viewmenu)

#about#
helpmenu = Menu(menubar,tearoff=0)
helpmenu.add_command(label="About",command=lambda:print("PYxis : Pre-release by Quaich @ Github"))
menubar.add_cascade(label="Help",menu=helpmenu)                     
master.config(menu=menubar)

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
w.bind("<Button-2>",dragstart)
w.bind("<B2-Motion>",dragend)
##zoom##
#Windows
if platform.system() == "Windows":  w.bind("<MouseWheel>",scroll)
#linux
if platform.system() == "Linux":
    w.bind("<Button-4>",scroll)
    w.bind("<Button-5>",scroll)
while True:
    if paused != True:
           otime = time.time()
           main()
           ##Pause safely##
           if tbp == True or tbpc == True:
                  if tbpc == True:
                         playpause(True)
                         askcolour(prevpaused)
                         playpause(False)
                         tbpc = False
                  else: playpause(False)
                
            ##Move the planets in time with the rest of the program.##
           #I decided not to function this to save on calling globals##
           for number in range(0,currr):
                  if OBJECTS[number][0] != "d" and OBJECTS[number][0] != "n":
                     w.move(OBJECTS[number][14],OBJECTS[number][6],OBJECTS[number][7])
                     oldxy = [((OBJECTS[number][0]+OBJECTS[number][2])/2),((OBJECTS[number][1]+OBJECTS[number][3])/2)]
                     try: OBJECTS[number][0],OBJECTS[number][1],OBJECTS[number][2],OBJECTS[number][3] = w.coords(OBJECTS[number][14])
                     except ValueError: pass
                     newxy = [((OBJECTS[number][0]+OBJECTS[number][2])/2),((OBJECTS[number][1]+OBJECTS[number][3])/2)]
                     if trail==True: drawtrail(oldxy,newxy,number,trail,planetcolour)
    w.update()
