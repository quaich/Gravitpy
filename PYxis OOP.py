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
w = Canvas(master, width=1200, height=1000) #generate 1200x1000 canvas
master.resizable(width=False,height=False)
w.pack() #packdat
master.iconbitmap("icon.ico")
currr = 0 #The row number in the 2d array "OBJECTS" that is avalible for use.
xforce = 0
yforce = 0
speed = 1
tbp = False
tbpc = False
trail = False
starttime = time.time()
lasttime = starttime
paused = False
prevpaused = False
imported = False
planetcolour = ((255,0,0),"#FF0000")
#constants
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



planetdict = {}
currentpos = 0
class planet():
    def __init__(self,x,y,xx,yy,mass,cstring,vx,vy,lx,ly,rad,R,G,B,atime,nom):
        self.count = 0
        self.x = x
        self.y = y
        self.xx = xx
        self.yy = yy
        self.mass = mass
        self.colours = cstring
        self.vx = vx
        self.vy = vy
        self.lx = lx
        self.ly = ly
        self.radius = radius
        self.red = R
        self.blue = B
        self.green = G
        self.alivetime = atime
        self.devoured = nom
        self.represent = 0
        self.create()
    def create(self):
        self.represent = w.create_oval(self.x,self.y,self.xx,self.yy,fill=self.colours,tags="p")
        w.lower("p")

class calculations():
    def maths(self,objectxy,object2xy,ere):
        a = int(objectxy[0] - object2xy[0])
        b = int(objectxy[1] - object2xy[1])
        xn,yn = False,False
        radius = math.sqrt(a**2 + b**2)
        if radius != 0:
            if a == 0:
                theta = 0
            else:
                theta = abs(math.atan(b/a))
        else:
            theta = 0
            radius = 1
        if ere != False:
            if b > 0:
                yn = True
            else:
                yn = False
            if a > 0:
                xn = True
            else:
                xn = False
            return(radius,theta,xn,yn)
        else:
            return(radius,theta)
    def physics(self,objectxy,object2xy):
        G = 6.6742
        radius,theta,xn,yn = self.maths(objectxy,object2xy,False)
        Fgrav = ((G*(int(mass1)*(int(mass2))))/radius**2) / mass1
        if xn == True:
            accelerationx = -Fgrav*math.cos(theta)
        else:
            accelerationx = Fgrav*math.cos(theta)
        if yn == True:
            accelerationy = -Fgrav*math.sin(theta)
        else:
            accelerationy = Fgrav*math.sin(theta)
        cspeed = int(uiinstance.speed.get())









class ui():
    def __init__(self):
        #Count for the total number of planets (replacement to currr).
        self.planetcount = 0

        #Values from the UI.
        self.colour = ((255,0,0),"#FF0000")
        self.density = 20

        #state of the program.
        self.paused = False

        #Default positional stance.
        self.ox = 0
        self.oy = 0

        #UI elements:
        #Button to play and pause the program.
        self.playpause =  Button(master,text="▐▐  ", command =lambda:self.safetypause(False),font=("Helvetica", 12))
        self.playpause.place(x=1150,y=5,width=30,height=30)

        #Button to load a file.
        self.loadbutton = Button(master,text="Load file",command=fileop.load)
        self.loadbutton.place(x=1060,y=415,width=80)

        #Button to save a file.
        self.savebutton = Button(master,text="Save file",command=fileop.save)
        self.savebutton.place(x=1060,y=385,width=80)

        #button to Toggle the Stars.
        self.starbutton = Button(master, text="Toggle Stars on", command=self.startoggle)
        self.stary.place(x=1040,y=150,width=120)

        #Text for running time and frames per second.
        self.runningtime = w.create_text(50,30,fill = "White")
        self.fps = w.create_text(150,30,fill="White")

        #Input for mass.

        self.mass = IntVar()
        self.mass.set(100) #Defualt mass
        w.create_text(1060,247,text= "Mass",font=("Helvetica", 10))
        self.Mass = Entry(master,width=10,textvariable=mass)
        self.Mass.place(x=1100,y=240)

        #Input for density

        self.density = IntVar()
        self.density.set(20) #Default density
        w.create_text(1065,277,text= "Density",font=("Helvetica",10))
        self.Density = Entry(master,width=10, textvariable=density)
        self.Density.place(x=1100,y=270)

        #Trail duration slider

        self.trailduration = IntVar()
        self.trailduration.set(0)
        w.create_text(1065,677,text="Trail duration\n(0 = ∞)",font=("Helvetica",10))
        self.trailduration = Scale(master,from_=0,to=20,orient=HORIZONTAL)
        self.trailduration.place(x=1100,y=670)

        #Planetary variables

        w.create_text(1100,495,text="Planet Information",font=("Helvetica",10,"bold underline"))

        w.create_text(1062,520,text="Velocity")
        self.planetvelocity = IntVar()
        self.showoffvelocity = Entry(master,width=6,textvariable=planetvelocity)
        self.showoffvelocity.place(x=1100,y=513)
        self.planetvelocity.set(0)
        self.showoffvelocity.configure(state="disabled")

        w.create_text(1062,550,text="Mass")
        self.planetmass = IntVar()
        self.showoffmass = Entry(master,width=6,textvariable=planetmass)
        self.showoffmass.place(x=1100,y=540)
        self.planetmass.set(0)
        self.showoffmass.configure(state="disabled")

        w.create_text(1062,572,text="Density")
        self.planetdensity = IntVar()
        self.showoffdensity = Entry(master,width=6,textvariable=planetdensity)
        self.showoffdensity.place(x=1100,y=567)
        self.planetdensity.set(0)
        self.showoffdensity.configure(state="disabled")

        w.create_text(1062,605,text="Devorered\n  planets")
        self.planetsdevoured = IntVar()
        self.showoffdevoured = Entry(master,width=6,textvariable=planetsdevoured)
        self.showoffdevoured.place(x=1100,y=595)
        self.planetsdevoured.set(0)
        self.showoffdevoured.configure(state="disabled")

        w.create_text(1062,635,text="Time alive")
        self.planetalivetime = IntVar()
        self.showoffalive = Entry(master,width=6,textvariable=planetalivetime)
        self.showoffalive.place(x=1100,y=625)
        self.planetalivetime.set(0)
        self.showoffalive.configure(state="disabled")

        w.create_text(1035,20,text="Force amp")
        self.speed = Scale(master,from_=1,to=100,resolution=1,variable=speed,orient=HORIZONTAL,bg="white",length = 50,width=20)
        self.speed.place(x=1085,y=5)

        #start with stars
        self.startoggle()
    def initialclick(self,event):
        x = event.x
        y = event.y
        self.intmass = int(mass.get())
        self.intden = int(density.get())
        if event.x < 1000:
            self.ox = event.x
            self.oy = event.y
            addrad = (self.intmass/self.intden)
            w.create_oval(x+addrad,y+addrad,x-addrad,y-addrad,self.colour[1],tags="shot")
    def motion(self,event):
        w.delete("sline")
        if event.x < 1000:
            w.create_line(self.ox,self.oy,event.x,event.y,fill=self.colour,tags="sline")
    def release(self,event):
        if event.x < 1000:
            lenx = event.x - self.ox
            leny = event.y - self.oy
            if self.mass < self.den:
                self.mass = self.den * 2
            radius = self.mass / self.den
            start = [ox,oy]
            end = [event.x,event.y]
            rad,theta = calculations.maths(start,end,True)
            vx = lenx/(self.intmass*5)
            vy = leny/(self.intmass*5)
            planetdict[self.planetcount] = planet(round(radius),self.intmass,self.ox,self.colour[0][0],self.colour[0][1],self.colour[0][2],xy,xy,theta)
            planetincrement()
        w.delete("sline")
        w.delete("shot")
    def safetypause(funct):
        if self.paused != True:
            tbp = True
            self.safetypause()
        if funct = "colour":
            self.changecolour()
        else:
            pass
    def planetincrement(self):
        self.planetcount += 1
    def changecolour(self):
        if self.paused != True:
            safetypause("colour")
        self.colour = askcolour()
    def move(self):





#keybinds

uiinstance = ui()

w.bind("<Button-1>",uiinstance.initalclick) #initial click
w.bind("<B1-Motion>",uiinstance.motion) #click and drag
w.bind("<ButtonRelease-1>",release) #release of click
w.bind("<Button-3>",selectobject)
'''
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


def physics(mainl,planets,objectxy,object2xy,exclude,OBJECTS,speed):
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

def Euler(objectxy,object2xy,mainl,planets,exclude,OBJECTS,speed):
       prevxy = objectxy
       vx,vy = physics(mainl,planets,objectxy,object2xy,exclude,OBJECTS,speed)
       OBJECTS[mainl][6] += vx
       OBJECTS[mainl][7] += vy


def createplanet(rad,mass,x,y,R,G,B,cx,cy,theta):
    global planetcolour
    global currr
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
    global currr
    global imported
    global OBJECTS
    global exclude
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
'''
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

w.create_text(1062,635,text="Time alive")
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
systemname = ("Gravitpy - System: {}{}-{}{}{}".format(alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],random.randint(0,9),random.randint(0,9),random.randint(0,9))) #Standard string consentraition methods leave ugly curly brackets.
master.wm_title(systemname)

##Startoggle##
startoggle()
#------------------------------------------UI SECTION END--------------------------------------#



while True:
    if paused != True:
           w.itemconfig(curtime,text=("Time",round(time.time() - starttime,2)))
           otime = time.time()
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
           if currr > 0 and OBJECTS[planetselected][0] != "d":
                  planetvelocity.set(math.sqrt(((OBJECTS[planetselected][6])**2) +  ((OBJECTS[planetselected][7])**2))*100)
                  planetmass.set(OBJECTS[planetselected][4])
                  planetdensity.set(OBJECTS[planetselected][4] / OBJECTS[planetselected][10])
                  planetalivetime.set(round(time.time() - OBJECTS[planetselected][15]))
                  planetsdevoured.set(OBJECTS[planetselected][17])
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
'''
