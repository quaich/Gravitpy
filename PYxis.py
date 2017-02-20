#TODO

#1. Make UI OO

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
w = Canvas(master, width=1200, height=1000) #generate 1200x1000 canvas
master.resizable(width=False,height=False)
w.pack() #packdat
try:
       master.iconbitmap("icon.ico")
except TclError:
       print("Icon not found. Continuing..")

#constants
G = 6.6742 #simplfied

#2d arrays
OBD = [] #2D dictionary for planet variables
poplist = []

def main():
       if len(OBD) > 1:
               for mainl in range(0,len(OBD)): #for more than one object
                       x = 0
                       alone = True
                       for lines in range(len(OBD)):
                            if mainl != lines:
                                   alone = False
                                   break
                       if alone == True:
                              solo(trail,planetcolour)
                       objectxy = [((OBD[mainl]["x0"]+OBD[mainl]["x1"])/2),((OBD[mainl]["y0"]+OBD[mainl]["y1"])/2)]
                       calculatedeltaXY(G,objectxy,mainl,OBD,speed)
                       OBD[mainl]["lx"] = objectxy [0]
                       OBD[mainl]["ly"] = objectxy [1]
       if len(OBD) == 1:
              solo(planetcolour)

def solo(planetcolour):
        #print(OBD[0])
        x = ((OBD[0]["x0"]+OBD[0]["x1"])/2)
        y = ((OBD[0]["y0"]+OBD[0]["y1"])/2)
        w.move(OBD[0]["planet"],OBD[0]["dx"],OBD[0]["dy"])
        OBD[0]["x0"],OBD[0]["y0"],OBD[0]["x1"],OBD[0]["y1"] = w.coords(OBD[0]["planet"])
        nx = ((OBD[0]["x0"]+OBD[0]["x1"])/2)
        ny = ((OBD[0]["y0"]+OBD[0]["y1"])/2)
        xy = [x,y]
        nxy = [nx,ny]
        if trailduration.get() > 0: drawtrail(xy,nxy,0,planetcolour)

def calculatedeltaXY(G,objectxy,mainl,OBD,speed):
        global poplist
        for planets in range(0,len(OBD)):
            if planets != mainl:
                object2xy = [((OBD[planets]["x0"]+OBD[planets]["x1"])/2),((OBD[planets]["y0"]+OBD[planets]["y1"])/2)]
                if object2xy != objectxy:
                           ###Essentialy the collision detection###
                           radius,theta,xn,yn = maths(objectxy,object2xy)
                           if colide(mainl,planets,radius) == True:
                                  if OBD[mainl]["radius"] >= OBD[planets]["radius"] and planets not in poplist:
                                         tbd = planets
                                         tbnd = mainl
                                         OBD[mainl]["mass"] += OBD[planets]["mass"]
                                         OBD[mainl]["planetsdevoured"] += 1
                                  elif OBD[planets]["radius"] >= OBD[mainl]["radius"] and mainl not in poplist:
                                         tbd = mainl
                                         tbnd = planets
                                         OBD[planets]["mass"] += OBD[mainl]["mass"]
                                         OBD[planets]["planetsdevoured"] += 1

                                  try:
                                         if tbd not in poplist and tbnd not in poplist:
                                             poplist.append(tbd)
                                  except UnboundLocalError: pass
                                  break
                           Euler(objectxy,object2xy,mainl,planets,OBD,speed)

def maths(objectxy,object2xy):
        a = int(objectxy[0] - object2xy[0])
        b = int(objectxy[1] - object2xy[1])
        xn = False
        yn = False
        radius = math.sqrt((a**2) + (b**2)) #Pythagorus theorem
        if radius != 0:
               if a == 0:
                      theta = 0 #change in x is 0 and we dont want an error to be thrown.
               else:
                      theta = abs(math.atan(b/a))
        else:
               theta = 0
        if -1 < radius < 1:
               radius = 1 #no div by 0
        if b > 0:
               yn = True
        else:
               yn = False
        if a > 0:
               xn = True
        else:
               xn = False
        return(radius,theta,xn,yn)

def physics(mainl,planets,objectxy,object2xy,OBD,speed):
       radius,theta,xn,yn = maths(objectxy,object2xy)
       if radius != 0:
              Fgrav = ((G*(int(OBD[mainl]["mass"])*(int(OBD[planets]["mass"]))))/radius**2) / OBD[mainl]["mass"]

              if xn == True:
                     accelerationx = -(Fgrav*math.cos(theta))
              else:
                     accelerationx = Fgrav*math.cos(theta)
              if yn == True:
                     accelerationy = -(Fgrav*math.sin(theta))
              else:
                     accelerationy = Fgrav*math.sin(theta)
              cspeed = (speed.get()/1000)
              #Resolving (Right) (positive x)
              vx = accelerationx*cspeed
              vy = accelerationy*cspeed
              #Resolving (Down) (positive y)
              return(vx,vy)

def Euler(objectxy,object2xy,mainl,planets,OBD,speed):
       prevxy = objectxy
       vx,vy = physics(mainl,planets,objectxy,object2xy,OBD,speed)
       OBD[mainl]["dx"] += vx
       OBD[mainl]["dy"] += vy

def createplanet(rad,mass,x,y,R,G,B,cx,cy,theta):
    global planetcolour
    global OBD
    OBD.append({"x0": x-rad,"y0": y-rad,"x1": x+rad, "y1": y+rad,"mass": mass,"RGB":('#%02x%02x%02x' % (int(R//1), int(G//1), int(B//1))),"dx":cx,"dy":cy,"lx":x,"ly":y,"radius":rad,"R":R,"G":G,"B":B,"planet":0,"alivetime":time.time(),"Theta":theta,"planetsdevoured":0})
    slot = (len(OBD)-1)
    OBD[slot]["planet"] = w.create_oval(OBD[slot]["x0"],OBD[slot]["y0"],OBD[slot]["x1"],OBD[slot]["y1"],fill=(OBD[slot]["RGB"]),tags="oval")
    w.lower("oval")
    w.lower("star")

def colide(mainl,planets,radius):
    if radius < OBD[mainl]["radius"]:
        w.lower(OBD[planets]["planet"])
        if radius < OBD[mainl]["radius"]:
               return True
    elif radius < OBD[planets]["radius"]:
        w.lower(OBD[mainl]["planet"])
        if radius < OBD[planets]["radius"]:
               return True
    else: return False

###UI Related subroutines###

def trailtoggle():
    global trail
    if trailbutton["text"] == "Toggle Trail on":
           trailbutton["text"] = "Toggle Trail off"
    else:
           trailbutton["text"] = "Toggle Trail on"
    trail = not trail

def drawtrail(prevxy,objectxy,mainl,planetcolour):
       global trailduration
       colour = planetcolour [1]
       trail = w.create_line(prevxy[0],prevxy[1],objectxy[0],objectxy[1],fill=OBD[mainl]["RGB"],tags="t")
       w.lower(trail)
       if trailduration.get() != 20:
              master.after(int((trailduration.get())*1000),lambda:w.delete(trail))

def playpause(colourc):
       global paused
       if colourc == True:
           if paused != True:
                  prevpaused = paused
                  playp["text"] = " ► "
                  paused = True
       elif colourc ==  False:
           if playp["text"] == "▐▐  ":
                  playp["text"] = " ► "
           else:
                  playp["text"] = "▐▐  "
           paused = not paused
       w.update()

def safetypause(colourc):
       global tbp
       if paused == True:
              playpause(colourc)
              tbp = False
       else:
              tbp = True

def clickfunct(event):
       global ox
       global oy
       global mass
       global density
       global planetcolour
       try:
              floatmass = float(mass.get())
              floatdensity = float(density.get())
              nmass = round(abs(floatmass))
              ndensity = round(abs(floatdensity))
              if event.x < 1000:
                     ox = event.x
                     oy = event.y
                     w.create_oval(event.x+(nmass/ndensity),event.y+(nmass/ndensity),event.x-(nmass/ndensity),event.y-(nmass/ndensity),fill=planetcolour[1],tags="shotoval")
       except TclError:
              print("Mass and/or density values are invalid.")
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
       try:
              lmass = int(mass.get()//1)
              ldensity = int(density.get()//1)       
              if lmass < ldensity:
                     lmass = ldensity *2
              radius = lmass / ldensity
              end = [x,y]
              start = [ox,oy]
              rad,theta,xneg,yneg= maths(start,end)
              vx = cx /(rad)
              vy = cy /(rad)
              createplanet(round(radius),lmass,ox,oy,planetcolour[0][0],planetcolour[0][1],planetcolour[0][2],vx,vy,theta)
       except TclError:
              pass
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
       try:
               x = planetcolour [1][0]
       except TypeError:
              planetcolour = ((255,0,0),"#FF0000")

def startoggle(): #make these shift all in one direction at some point
    if stary["text"] == "Toggle Stars off":
        w.delete("star")
        stary["text"] = "Toggle Stars on"
    else:
        for i in range(0,1000):
            for x in range(0,1): #make this variable
                ran = random.randint(0,1000)
                colourcode = random.randint(0,255)
                w.create_oval(ran,i,ran,i,outline=('#%02x%02x%02x' % (colourcode,colourcode, colourcode)),tags="star")
        w.lower("star")
        stary["text"] = "Toggle Stars off"

###LOAD AND SAVE SYSTEM###
def load(quick):
    #variables to be edited#
    global OBD
    sfile = ""
    if quick == False:
           file = filedialog.askopenfilename(filetypes=[(".pyx Format","*.pyx")],title="Choose a file to load")
    else:
           file ="tmp.pyx"
    try:
       with open(file,'r') as load:
             temparray = []
             ##Reset Variables##
             systemname = ("PYxis - System: {}".format(file))
             master.wm_title(systemname)
             w.delete("t")
             ###Delete array###
             OBD = []
             ###set array to the file###
             lines = [line.split() for line in load]
             for line in range(0,len(lines)):
                    temparray.append(lines[line])
             w.delete("oval")
             ###convert to float###
             for y in range(0,len(temparray)):
                     for x in range(len(temparray[y])):
                            try: temparray[y][x] = float(temparray[y][x])
                            except ValueError: pass #cant convert strings to float
       for lines in range(0,len(temparray)):
            createplanet(temparray[lines][10],temparray[lines][4],((temparray[lines][0]+temparray[lines][2])/2),((temparray[lines][1]+temparray[lines][3])/2),temparray[lines][11],temparray[lines][12],temparray[lines][13],temparray[lines][6],temparray[lines][7],0)
    except FileNotFoundError:
            print("FILE: No file was found.")
    except IndexError:
            print("Invalid File.") 

def save(quick):
    global OBD
    if quick == True:
           file = open("tmp.pyx","w")
    else:
           file = filedialog.asksaveasfile(filetypes=[(".pyx Format","*.pyx")],title="Choose a file to save",defaultextension=".gpy")
    for lines in range(len(OBD)):
             array = [OBD[lines]["x0"],OBD[lines]["y0"],OBD[lines]["x1"],OBD[lines]["y1"],OBD[lines]["mass"],OBD[lines]["RGB"],OBD[lines]["dx"],OBD[lines]["dy"],OBD[lines]["lx"],OBD[lines]["ly"],OBD[lines]["radius"],OBD[lines]["R"],OBD[lines]["G"],OBD[lines]["B"],OBD[lines]["planet"],OBD[lines]["alivetime"],OBD[lines]["Theta"],OBD[lines]["planetsdevoured"]]
             for entitiy in array:
                 file.write(str(entitiy))
                 file.write(" ")
             file.write(" \n")
    file.close()

def popplanets():
    global OBD
    global poplist
    for planet in range(len(poplist)):
        try:
               w.delete(OBD[poplist[planet]]["planet"])
               OBD.pop(poplist[planet])
        except:
               print("Whoopsies")
    poplist = []

def selectobject(event):
       x = event.x
       y = event.y
       closest = w.find_closest(x,y)
       try:
              if w.gettags(closest)[0] == "oval":
                     coords = w.coords(closest)
                     for i in range(0,len(OBD)):
                            if coords == [OBD[i]["x0"],OBD[i]["y0"],OBD[i]["x1"],OBD[i]["y1"]]:
                                         global planetselected
                                         planetselected = i
              else: print("INFO: There's no planets around here!")
       except: pass
def deltrail():
       w.delete("t")

#------------------------------------------UI SECTION------------------------------------------#

#Basic UI elements#
starttime = time.time()
lasttime = starttime
w.configure(background="Black")#Main background
optionsbackground = w.create_rectangle(1001,0,1205,1000,fill="white") #white rectangle behind the options
curtime = w.create_text(50,30,fill = "White") #Time running
fps = w.create_text(150,30,fill = "White") #current FPS
ox = 0
oy = 0

#Pause related#
tbp = False
tbpc = False
paused = False
prevpaused = False
playp = Button(master,text="▐▐  ", command =lambda:safetypause(False),font=("Helvetica", 12))
playp.place(x=1130,y=120,width=30,height=27)


#Delete trails#
deltrailb = Button(master,text="Delete Trails",command=deltrail)
deltrailb.place(x=1040,y=120,width=80)

#Planet colour chooser#
planetcolour = ((255,0,0),"#FF0000") #default planetcolour
colourchoose = Button(master,text="Select colour",command=lambda:getcolour(prevpaused))
colourchoose.place(x=1040,y=300,width = 120)

#load and save#
loadfunct = Button(master,text="Load file",command=lambda:load(False))
loadfunct.place(x=1110,y=415,width=60)

quickloadfunct = Button(master,text="Quick Load",command=lambda:load(True))
quickloadfunct.place(x=1030,y=415,width=70)

savefunct = Button(master,text="Save file",command=lambda:save(False))
savefunct.place(x=1110,y=385,width=60)

quicksavefunct = Button(master,text="Quick save",command=lambda:save(True))
quicksavefunct.place(x=1030,y=385,width=70)

#toggle stars#
stary = Button(master, text="Toggle Stars on", command=startoggle)
stary.place(x=1040,y=150,width=120)



###Planet specific variables###
w.create_rectangle(1020,50,1180,190,fill="Light Grey") #toggle function box
w.create_rectangle(1020,675,1180,760,fill="Light Grey")
w.create_rectangle(1020,200,1180,340,fill="Light Grey")
w.create_rectangle(1020,350,1180,450,fill="Light Grey")
w.create_rectangle(1001,460,1250,470,fill="BLACK")
w.create_rectangle(1020,480,1180,660,fill="Light Grey")
w.create_text(1100,63,text="Misc Functions",font=("Helvetica",10,"bold underline"))
w.create_text(1100,366,text="Load and save",font=("Helvetica",10,"bold underline"))
w.create_text(1100,215,text="Planet Properties",font=("Helvetica",10,"bold underline"))

#Mass#

mass = DoubleVar()
mass.set(100)
w.create_text(1060,247,text= "Mass",font=("Helvetica", 10))
Mass = Entry(master,width=10,textvariable=mass)
Mass.place(x=1100,y=240)

#Density#

density = DoubleVar()
density.set(20)
w.create_text(1065,277,text= "Density",font=("Helvetica",10))
Density = Entry(master,width=10, textvariable=density)
Density.place(x=1100,y = 270)

#Trail Duration#

trailduration = IntVar()
trailduration.set(0)
trailduration = Scale(master,from_=0,to=20,orient=HORIZONTAL,bg="light grey",highlightthickness=0)
trailduration.place(x=1050,y=715)
w.create_text(1100,700,text="Trail duration\n      (20 = ∞)",font=("Helvetica",10,"bold"))

#Force Amplification

speed = 1 #forceamp
w.create_text(1070,100,text="Force amp")
speed = Scale(master,from_=1,to=2,resolution=0.01,variable=speed,orient=HORIZONTAL,length = 50,width=20,bg="light grey",highlightthickness=0)
speed.place(x=1110,y=70)

#Planet variable showing#
planetselected = 0

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

###    TITLE    ###
alphabet = []
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
           if len(poplist) > 0:
               popplanets()
           main()


           ##Pause safely##
           if tbp == True or tbpc == True:
                  if tbpc == True:
                         playpause(True)
                         askcolour(prevpaused)
                         playpause(False)
                         tbpc = False
                  else: playpause(False)
           ##Selected planet attributes##
           if len(OBD) -1 > 0:
                  planetvelocity.set(math.sqrt(((OBD[planetselected]["dx"])**2) +  ((OBD[planetselected]["dy"])**2))*1000)
                  planetmass.set(OBD[planetselected]["mass"])
                  planetdensity.set(OBD[planetselected]["mass"] / OBD[planetselected]["radius"])
                  planetalivetime.set(round(time.time() - OBD[planetselected]["alivetime"]))
                  planetsdevoured.set(OBD[planetselected]["planetsdevoured"])
           ##Move the planets in time with the rest of the program.##
           #I decided not to function this to save on calling globals##
           for number in range(0,len(OBD)):
                     w.move(OBD[number]["planet"],OBD[number]["dx"],OBD[number]["dy"])
                     if number == planetselected:
                         w.delete("s")
                         selected = w.coords(OBD[number]["planet"])
                         try:
                             selectoval = w.create_oval(selected[0]-10,selected[1]-10,selected[2]+10,selected[3]+10,outline = "yellow",stipple="gray75",tags="s" )
                         except IndexError:
                             print("INFO : Planet was destroyed, defaulting to 0.")
                             try:
                                  planetselected = 0
                             except IndexError:
                                 print("INFO : All planets are destroyed.")
                     oldxy = [((OBD[number]["x0"]+OBD[number]["x1"])/2),((OBD[number]["y0"]+OBD[number]["y1"])/2)]
                     try: OBD[number]["x0"],OBD[number]["y0"],OBD[number]["x1"],OBD[number]["y1"]= w.coords(OBD[number]["planet"])
                     except ValueError: pass
                     newxy = [((OBD[number]["x0"]+OBD[number]["x1"])/2),((OBD[number]["y0"]+OBD[number]["y1"])/2)]
                     if trailduration.get() > 0:
                            drawtrail(oldxy,newxy,number,planetcolour)
           try:
                  w.itemconfig(fps,text=("FPS:", round(1/(time.time()-otime))))
           except ZeroDivisionError:
                  pass #if the time change is too low
    w.update()
