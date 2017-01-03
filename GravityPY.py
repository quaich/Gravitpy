#TODO
#1.Fix the bug where planets "Forget" their varibales.
#2.Fix collision detection.
#3.Work on different intergration methods such as RK4 and Verlet.
#4.Do anything else that was highlighted on my initial objectives.
#5.Code efficiency/OOP approach to program,

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
w = Canvas(master, width=1200, height=1000) #generate 1000x1000 canvas
master.resizable(width=False,height=False)
w.pack() #packdat
#master.iconbitmap("icon.ico")
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
OBJECTS = [["n" for x in range(17)] for y in range(1000)]#(Y,X) #2d array for planet variables
exclude = [] #temporary mesure
disco = False
imported = False
planetcolour = ((255,255,255),"#ffffff")
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
                       calculatedeltaXY(currr,G,objectxy,list1,mainl,exclude)
                       OBJECTS[mainl][8] = objectxy [0]
                       OBJECTS[mainl][9] = objectxy [1]
       if currr == 1: #for an initial object
              x = ((OBJECTS[0][0]+OBJECTS[0][2])/2)
              y = ((OBJECTS[0][1]+OBJECTS[0][3])/2)
              w.move(OBJECTS[0][14],OBJECTS[0][6],OBJECTS[0][7])
              OBJECTS[0][0],OBJECTS[0][1],OBJECTS[0][2],OBJECTS[0][3] = w.coords(OBJECTS[0][14])
              nx = ((OBJECTS[0][0]+OBJECTS[0][2])/2)
              ny = ((OBJECTS[0][1]+OBJECTS[0][3])/2)
              xy = [x,y]
              nxy = [nx,ny]
              if trail == True: drawtrail(xy,nxy,0)

def calculatedeltaXY(currr,G,objectxy,list1,mainl,exclude):
        for planets in range(0,currr):
            if OBJECTS[planets][0] != "n":
                object2xy = [((OBJECTS[planets][0]+OBJECTS[planets][2])/2),((OBJECTS[planets][1]+OBJECTS[planets][3])/2)]
                list2 = (OBJECTS[planets][0],OBJECTS[planets][1],OBJECTS[planets][2],OBJECTS[planets][3])
                if list1 == list2: continue
                if planets == mainl: continue
                if planets in exclude: continue
                if OBJECTS[planets][0] != "n":
                    ###Calc variables##
                    ###EULER###
                    if default.get() == "Euler 8x" or default.get() == "Euler":
                            if default.get() == "Euler": step = 0
                            if default.get() == "Euler 4x": step = 4
                            Euler(objectxy,object2xy,mainl,planets,step,exclude)
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
        if radius == 0:
               radius = 1
        if b > 0: yn = True
        else: yn = False
        if a > 0: xn = True
        else: xn = False
        return(radius,theta,xn,yn)

def physics(mainl,planets,objectxy,object2xy,step,exclude):
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
       if colide(mainl,planets,radius) == True:
           accelerationx = 0
           accelerationy = 0
       vx = accelerationx*currenttime / (step+1)
       vy = accelerationy*currenttime / (step+1)
       #Resolving (Down) (positive y)
       return(vx,vy)

def Euler(objectxy,object2xy,mainl,planets,step,exclude):
       prevxy = objectxy
       for hop in range(0,step+1):
              if mainl not in exclude:
                  vx,vy = physics(mainl,planets,objectxy,object2xy,step,exclude)
                  OBJECTS[mainl][6] += vx
                  OBJECTS[mainl][7] += vy
                  w.move(OBJECTS[mainl][14],OBJECTS[mainl][6],OBJECTS[mainl][7])
                  OBJECTS[mainl][0],OBJECTS[mainl][1],OBJECTS[mainl][2],OBJECTS[mainl][3] = w.coords(OBJECTS[mainl][14])
                  objectxy = [((OBJECTS[mainl][0]+OBJECTS[mainl][2])/2),((OBJECTS[mainl][1]+OBJECTS[mainl][3])/2)]
       if trail == True: drawtrail(prevxy,objectxy,mainl)
       colour = toggle()
       if colour != "White":
              w.itemconfig(OBJECTS[mainl][14],fill = colour)
              colour = toggle()
              OBJECTS[mainl][5] = colour
       w.update()

def createplanet(rad,mass,x,y,R,G,B,cx,cy):
    global planetcolour
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
    colour = toggle()
    if imported == True: colour = '#%02x%02x%02x' % ((int(OBJECTS[currr][11]//1), int(OBJECTS[currr][12]//1), int(OBJECTS[currr][13]//1)))
    if colour == "White": OBJECTS[currr][5] = planetcolour[1]
    else: OBJECTS[currr][5] = colour
    OBJECTS[currr][14] = w.create_oval(OBJECTS[currr][0],OBJECTS[currr][1],OBJECTS[currr][2],OBJECTS[currr][3],fill=OBJECTS[currr][5],tags="oval")
    currr +=1
    w.lower("oval")
    w.update()

def colide(mainl,planets,radius):  #this "clipping" bullshit doesnt work and makes the program highly inaccurate. THis needs to be reworked into a working collision model.
    if radius < OBJECTS[mainl][10]:
        w.lower(OBJECTS[planets][14])
        if radius < 0.1*OBJECTS[mainl][14]:
            return True
    elif radius < OBJECTS[planets][10]:
        w.lower(OBJECTS[mainl][14])
        if radius < 0.1*OBJECTS[planets][10]: return True
    else: return False

###UI Related subroutines###

def debugtoggle():
    global debug
    if debug == False:
        for i in range(1,10):
            lfill = "red"
            if i == 5: lfill = "green"
            w.create_line(100*i,0,100*i,1000,fill=lfill, dash = (4,4),tags="debug")
            w.create_line(0,100*i,1000,100*i,fill=lfill, dash = (4,4),tags="debug")
        w.create_line(0, 0, 1000, 1000, fill="red", dash=(4, 4),tags="debug")
        w.create_line(0, 1000, 1000, 0, fill="red", dash=(4, 4),tags="debug")
        #curtime = w.create_text(50,100,fill = "White",tags="debug")
        #fps = w.create_text(50,150,fill = "White",tags="debug")
    else:
        w.delete("debug")
    debug = not debug
def fml():
	global disco
	disco = not disco
	w.configure(background="Black")
def trailtoggle(currr):
    global trail
    if trail == True:
           w.delete()
           trailbutton["text"] = "Toggle Trail on"
           w.delete("t")
    else:
           trailbutton["text"] = "Toggle Trail off"

    trail = not trail

def drawtrail(prevxy,objectxy,mainl):
       if trail == True:
           colour = toggle()
           if colour == "White":
                global planetcolour
                colour = planetcolour [1]
           w.create_line(prevxy[0],prevxy[1],objectxy[0],objectxy[1],fill=OBJECTS[mainl][5],tags="t",)
       w.lower("t")

def playpause():
       global paused
       if playpause["text"] == "▐▐  ": playpause["text"] = " ► "
       else: playpause["text"] = "▐▐  "
       paused = not paused

def clickfunct(event):
       global ox
       global oy
       ox = event.x
       oy = event.y
       w.create_oval(event.x+2,event.y+2,event.x-2,event.y-2,fill="#FF00EA",tags="shot")

def motion(event):
       w.delete("shot")
       colour = toggle()
       if colour == "White": colour = "Blue"
       w.create_line(ox,oy,event.x,event.y,fill=colour,tags="shot")

def release(event):
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
       createplanet(round(radius),lmass,ox,oy,planetcolour[0][0],planetcolour[0][1],planetcolour[0][2],vx,vy)
def toggle():
     if disco == True: return('#%02x%02x%02x' % (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
     else: return("White")
def getcolour():
    global planetcolour
    planetcolour = askcolor()

###LOAD AND SAVE SYSTEM###
def load():
       global imported
       imported = True
       file = filedialog.askopenfilename(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to load")
       with open(file,'r') as load:
             lines = [line.split() for line in load]
             OBJECTS = lines
             y = 0
             for row in OBJECTS:
                    for entity in row:
                           xd = "n"
             w.delete("oval","t")
             for x in lines:
                     try: OBJECTS[y][0] = float(OBJECTS[y][0])
                     except: break
                     OBJECTS[y][1] = float(OBJECTS[y][1])
                     OBJECTS[y][2] = float(OBJECTS[y][2])
                     OBJECTS[y][3] = float(OBJECTS[y][3])
                     OBJECTS[y][4] = float(OBJECTS[y][4])
                     OBJECTS[y][6] = float(OBJECTS[y][6])
                     OBJECTS[y][7] = float(OBJECTS[y][7])
                     OBJECTS[y][8] = float(OBJECTS[y][8])
                     OBJECTS[y][9] = float(OBJECTS[y][9])
                     OBJECTS[y][10] = float(OBJECTS[y][10])
                     OBJECTS[y][11] = float(OBJECTS[y][11])
                     OBJECTS[y][12] = float(OBJECTS[y][12])
                     OBJECTS[y][13] = float(OBJECTS[y][13])
                     try:
                            OBJECTS[y][15] = float(OBJECTS[y][15])
                            OBJECTS[y][16] = float(OBJECTS[y][16])
                     except: print("k lol")
                     y+=1
             OBJECTS = lines
       i = 0
       for lines in OBJECTS:
            if OBJECTS[i][0] == "n":
                     global currr
                     currr = i
                     break
            createplanet(OBJECTS[i][10],OBJECTS[i][4],((OBJECTS[i][0]+OBJECTS[i][2])/2),((OBJECTS[i][1]+OBJECTS[i][3])/2),OBJECTS[i][11],OBJECTS[i][12],OBJECTS[i][13],OBJECTS[i][6],OBJECTS[i][7])
            i += 1
      # except:
      #        print("An error occured")
def save():
       file = filedialog.asksaveasfile(filetypes=[(".gpy Format","*.gpy")],title="Choose a file to save")
       for lines in OBJECTS:
              for entity in lines:
                     file.write(str(entity))
                     file.write(" ")
              file.write("\n")
def startoggle(): #make these shift all in one direction at some point
    for i in range(0,1000):
        for x in range(0,1): #make this variable
            ran = random.randint(0,1000)
            w.create_oval(ran,i,ran,i,outline="White",tags="star")





#------------------------------------------UI SECTION------------------------------------------#
###A E S T H E T I C S###
w.configure(background="Black")
b1 = w.create_rectangle(1001,0,1205,1000,fill="white")

playpause = Button(master,text="▐▐  ", command=playpause,font=("Helvetica", 12))
playpause.place(x=1100,y=5,width=30,height=30)

trailbutton = Button(master, text="Toggle Trail off", command=lambda: trailtoggle(currr))
trailbutton.place(x=1100,y=100,width=100)

stary = Button(master, text="Toggle Stars",command=startoggle)
stary.place(x=1100,y=300,width=100)






discotrail = Button(master,command=fml)
discotrail.place(x=1190,y=0,width=10,height=10)

colourchoose = Button(master,text="Select colour",command=getcolour)
colourchoose.place(x=1100,y=160,width = 100)


loadfunct = Button(master,text="Load file",command=load)
loadfunct.place(x=1010,y=160,width=80)

savefunct = Button(master,text="Save file",command=save)
savefunct.place(x=1010,y=130,width=80)

debuglines = Button(master, text="Toggle Debug", command=debugtoggle)
debuglines.place(x=1100,y=130,width=100)
curtime = w.create_text(50,100,fill = "White")
fps =     w.create_text(50,150,fill = "White")
###Planet specific variables###
b2 = w.create_rectangle(1020,200,1180,300,fill="Light Grey")

w.create_text(1040,63,text="Intergration \nMethod")

#Mass#
mass = IntVar()
mass.set(100)
w.create_text(1060,227,text= "Mass",font=("Helvetica", 10))
Mass = Entry(master,width=10,textvariable=mass)
Mass.place(x=1100,y=220)
#Density#
density = IntVar()
density.set(20)
w.create_text(1065,267,text= "Density",font=("Helvetica",10))
Density = Entry(master,width=10, textvariable=density)
Density.place(x=1100,y = 260)


###    TITLE    ###

for alpha in range (65,91): alphabet.append(chr(alpha))  #something like that
systemname = ("Gravitpy - System: {}{}-{}{}{}".format(alphabet[random.randint(0,25)],alphabet[random.randint(0,25)],random.randint(0,9),random.randint(0,9),random.randint(0,9))) #Standard string consentraition methods leave ugly curly brackets.
master.wm_title(systemname)

###Dropdown  box###
default = StringVar(master)
default.set("Euler")
integration = OptionMenu(master,default,"Euler","Euler 4x","Euler legacy","RK4","Verlet")
integration.config(bg = "White",bd=0,fg="BLACK",activeforeground="BLACK")
integration["menu"].config(bg="White",fg="Black")
integration.place(x=1085,y=50,width=105)
###debug lines###
#debugtoggle()
startoggle()
#------------------------------------------UI SECTION END--------------------------------------#
#keybinds
w.bind("<Button-1>",clickfunct) #initial click
w.bind("<B1-Motion>",motion) #click and drag
w.bind("<ButtonRelease-1>",release) #release of click
while True:
    if paused == False:
           colour = toggle()
           if colour != "White":
                  colour = toggle()
           try:
                  w.itemconfig(curtime,text=("Time",round(time.time() - starttime,2)))
           except TclError:
                  pass
           otime = time.time()
           main()
           try:
                  w.itemconfig(fps,text=("FPS:", round(1/(time.time()-otime))))
           except ZeroDivisionError:
                  pass
           w.lower("trail")
    else:
           pass
    w.update()
