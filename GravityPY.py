#setup
#Importing modules
from tkinter import * #enables use of the Tkinter UI, responsible for drawing of objects and generation of GUI
import time #needed for restriction of refresh rate (may not be needed)
import math #needed for physics calculation
import random #for some more fun parts of the program.
import datetime #for delta time calculations
#functions and variables
#many of these variables can easily be locatlised.
master = Tk() #master window
alphabet=[]
w = Canvas(master, width=1200, height=1000) #generate 1000x1000 canvas
master.resizable(width=False,height=False)
w.pack() #packdat
currr = 0 #The row number in the 2d array "OBJECTS" that is avalible for use.
rad = 0 #radius
numberofplanets=0 #duh
xforce = 0
yforce = 0
planets = 0
list1 = 0
lines = True
xn = True
yn = True
trail = True
debug = False
starttime = time.time()
lasttime = starttime
#constants
G = 6.673 #simplfied
objectxy = []
ox = 0
oy = 0
#2d arrays
paused = False
OBJECTS = [["n" for x in range(17)] for y in range(100)]#(Y,X) #2d array for planet variables
"""
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
15 = prev time
16 = theta
"""
def main():
       if currr > 1:
               for mainl in range(0,currr): #for more than one object
                   if OBJECTS[mainl][0] != "n":
                       list1 = (OBJECTS[mainl][0],OBJECTS[mainl][1],OBJECTS[mainl][2],OBJECTS[mainl][3])
                       objectxy = [((OBJECTS[mainl][0]+OBJECTS[mainl][2])/2),((OBJECTS[mainl][1]+OBJECTS[mainl][3])/2)]
                       calculatedeltaXY(currr,G,objectxy,list1,mainl)
                       OBJECTS[mainl][8] = objectxy [0]
                       OBJECTS[mainl][9] = objectxy [1]
       if currr == 1: #for an initial object
              x = ((OBJECTS[0][0]+OBJECTS[0][2])/2)
              y = ((OBJECTS[0][1]+OBJECTS[0][3])/2)
              w.move(OBJECTS[0][14],OBJECTS[0][6],OBJECTS[0][7])
              OBJECTS[0][0],OBJECTS[0][1],OBJECTS[0][2],OBJECTS[0][3] = w.coords(OBJECTS[0][14])
              nx = ((OBJECTS[0][0]+OBJECTS[0][2])/2)
              ny = ((OBJECTS[0][1]+OBJECTS[0][3])/2)
              if trail == True: w.create_line(x,y,nx,ny,fill = "White",tags="trail")

def calculatedeltaXY(currr,G,objectxy,list1,mainl):
        for planets in range(0,currr):
            if OBJECTS[planets][0] != "n":
                object2xy = [((OBJECTS[planets][0]+OBJECTS[planets][2])/2),((OBJECTS[planets][1]+OBJECTS[planets][3])/2)]
                list2 = (OBJECTS[planets][0],OBJECTS[planets][1],OBJECTS[planets][2],OBJECTS[planets][3])
                if list1 == list2: continue
                if planets == mainl: continue
                if OBJECTS[planets][0] != "n":
                    ###Calc variables##
                    ###EULER###
                    if default.get() == "Euler 8x" or default.get() == "Euler":
                            if default.get() == "Euler": step = 0
                            if default.get() == "Euler 8x": step = 8
                            Euler(objectxy,object2xy,mainl,planets,step)
                    if default.get() == "Trapezium": Trapeziumrule(objectxy,object2xy)
                    if default.get() == "Verlet": xforce,yforce = Verlet(yn,xn,yforce,xforce,force,theta,step,planets)
                    if default.get() == "Runge-Kutta": Runge()
                    if default.get() == "RK4": RK4()
                    
def maths(objectxy,object2xy):
        a = int(objectxy[0] - object2xy[0])
        b = int(objectxy[1] - object2xy[1])
        xn = False
        yn = False
        #print("a",a,"b",b)
        radius = math.sqrt((a**2) + (b**2)) #Pythagorus theorem
        if radius != 0:
               if a == 0 : theta = 0 #change in x is 0 and we dont want an error to be thrown.
               else: theta = abs(math.atan(b/a))
        else: theta = 0
        if b > 0: yn = True
        else: yn = False
        if a > 0: xn = True
        else: xn = False
        return(radius,theta,xn,yn)
       
def physics(mainl,planets,objectxy,object2xy,step):
       radius,theta,xn,yn = maths(objectxy,object2xy)
       if radius == 0: pass
       Fgrav = ((G*(int(OBJECTS[mainl][4])*(int(OBJECTS[planets][4]))))/radius**2) / OBJECTS[mainl][4]
       if xn == True: accelerationx = -(Fgrav*math.cos(theta))
       else: accelerationx = Fgrav*math.cos(theta)
       if yn == True: accelerationy = -(Fgrav*math.sin(theta))
       else: accelerationy = Fgrav*math.sin(theta)
       currenttime = time.time() - otime
       #print("TIME",currenttime)
       #Resolving (Right) (positive x)
       vx = accelerationx*currenttime / (step+1)
       vy = accelerationy*currenttime / (step+1)
       #Resolving (Down) (positive y)
       return(vx,vy)

def Euler(objectxy,object2xy,mainl,planets,step):
       for hop in range(0,step+1):
              vx,vy = physics(mainl,planets,objectxy,object2xy,step)
              OBJECTS[mainl][6] += vx
              OBJECTS[mainl][7] += vy
              w.move(OBJECTS[mainl][14],OBJECTS[mainl][6],OBJECTS[mainl][7])
              OBJECTS[mainl][0],OBJECTS[mainl][1],OBJECTS[mainl][2],OBJECTS[mainl][3] = w.coords(OBJECTS[mainl][14])
              prevxy = objectxy
              objectxy = [((OBJECTS[mainl][0]+OBJECTS[mainl][2])/2),((OBJECTS[mainl][1]+OBJECTS[mainl][3])/2)]
              if trail == True: drawtrail(prevxy,objectxy)
              w.update()

def createplanet(rad,mass,x,y,R,G,B,cx,cy):
    global currr
    OBJECTS[currr][0] = x-rad
    OBJECTS[currr][1] = y-rad
    OBJECTS[currr][2] = x+rad
    OBJECTS[currr][3] = y+rad
    OBJECTS[currr][4] = mass
    OBJECTS[currr][6] = cx
    OBJECTS[currr][7] = cy
    OBJECTS[currr][8] = x
    OBJECTS[currr][9] = y
    OBJECTS[currr][10] = rad
    OBJECTS[currr][11] = R
    OBJECTS[currr][12] = G
    OBJECTS[currr][13] = B
    OBJECTS[currr][5] = '#%02x%02x%02x' % (OBJECTS[currr][11],OBJECTS[currr][12],OBJECTS[currr][13])
    OBJECTS[currr][14] = w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill=OBJECTS[currr][5],tags="oval")
    currr +=1
    w.lower("oval")
    w.update()
    
def debugtoggle():
    global debug
    if debug == False:
        curtime = w.create_text(50,100,fill = "White",tags="debug")
        for i in range(1,10):
            lfill = "red"
            if i == 5: lfill = "green"
            w.create_line(100*i,0,100*i,1000,fill=lfill, dash = (4,4),tags="debug")
            w.create_line(0,100*i,1000,100*i,fill=lfill, dash = (4,4),tags="debug")
        w.create_line(0, 0, 1000, 1000, fill="red", dash=(4, 4),tags="debug")
        w.create_line(0, 1000, 1000, 0, fill="red", dash=(4, 4),tags="debug")
    else:
        w.delete("debug")
    debug = not debug
    
def trailtoggle(currr):
    global trail
    if trail == True:
           w.delete("trail")
           trailbutton["text"] = "Toggle Trail on"
    else:
           trailbutton["text"] = "Toggle Trail off"
    trail = not trail
    
def drawtrail(prevxy,objectxy):
       if trail == True:
              w.create_line(prevxy[0],prevxy[1],objectxy[0],objectxy[1],fill="white",tags="trail")
              trailbutton["text"] = "Toggle Trail off"
       w.lower("trail")
       
def playpause():
       global paused
       if playpause["text"] == " ► ":
              playpause["text"] = "▐▐  "
       else:
              playpause["text"] = " ► "
       paused = not paused

def clickfunct(event):
       global ox
       global oy
       ox = event.x
       oy = event.y
       
def motion(event):
       w.delete("shot")
       w.create_line(ox,oy,event.x,event.y,fill="Blue",tags="shot")
       
def release(event):
       x = event.x
       y = event.y
       cx = event.x - ox
       cy = event.y - oy
       w.delete("shot")
       lmass = int(mass.get())
       ldensity = int(density.get())
       radius = lmass / ldensity
       G = round(255/(lmass))*40
       B = round(G)
       end = [x,y]
       start = [ox,oy]
       rad,theta,xneg,yneg= maths(start,end)
       vx = cx/((lmass)*5)
       vy = cy/((lmass)*5)
       createplanet(round(radius),lmass,ox,oy,255,G,B,vx,vy)

#------------------------------------------UI SECTION------------------------------------------#
###A E S T H E T I C S###
w.configure(background="Black")
b1 = w.create_rectangle(1001,0,1200,1000,fill="white")

playpause = Button(master,text=" ► ", command=playpause,font=("Helvetica", 12))
playpause.place(x=1015,y=5,width=30,height=30)

trailbutton = Button(master, text="Toggle Trail off", command=lambda: trailtoggle(currr))
trailbutton.place(x=1085,y=100,width=100)

debuglines = Button(master, text="Toggle Debug", command=debugtoggle)
debuglines.place(x=1085,y=130,width=100)
curtime = w.create_text(50,100,fill = "White",tags="debug")
fps =     w.create_text(50,150,fill = "White",tags="debug")
###Planet specific variables###
b2 = w.create_rectangle(1020,180,1180,300,fill="Light Grey")

w.create_text(1040,63,text="Intergration \nMethod")

#Mass#
mass = IntVar()
mass.set(100)
w.create_text(1060,210,text= "Mass",font=("Helvetica", 10))
Mass = Entry(master,width=10,textvariable=mass)
Mass.place(x=1100,y=200)
#Density#
density = IntVar()
density.set(20)
w.create_text(1065,240,text= "Density",font=("Helvetica",10))
Density = Entry(master,width=10, textvariable=density)
Density.place(x=1100,y = 230)


###    TITLE    ###

for alpha in range (65,91): alphabet.append(chr(alpha))  #something like that
systemname = ("Gravitpy - System: {}{}-{}{}{}".format(alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],random.randint(0,9),random.randint(0,9),random.randint(0,9))) #Standard string consentraition methods leave ugly curly brackets.
master.wm_title(systemname)

###Dropdown  box###
default = StringVar(master)
default.set("Euler")
integration = OptionMenu(master,default,"Euler","Euler 8x","Euler legacy","RK4","Verlet")
integration.config(bg = "White",bd=0,fg="BLACK",activeforeground="BLACK")
integration["menu"].config(bg="White",fg="Black")
integration.place(x=1085,y=50,width=105)
###debug lines###
debugtoggle()
#------------------------------------------UI SECTION END--------------------------------------#
#keybinds
w.bind("<Button-1>",clickfunct) #initial click
w.bind("<B1-Motion>",motion) #click and drag
w.bind("<ButtonRelease-1>",release) #release of click
while True:
    if paused == False:
           try:
                  w.itemconfig(curtime,text=round(time.time() - starttime,4))
           except TclError:
                  pass
           otime = time.time()
           main()
           try:
                  w.itemconfig(fps,text=round(1/(time.time()-otime)))
           except ZeroDivisionError:
                  pass
           w.lower("trail")
    else:
           pass
    w.update()
