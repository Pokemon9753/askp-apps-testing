from PIL import Image, ImageTk
from Tkinter import *

from tkColorChooser import askcolor
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
from msvcrt import getch

WHICHIMAGE=0
actionsarray=["Draw","Circle","Erase","Color","Change Background Color","Add Image"]
WHATAMIDOING = 0 
lastx=""
lasty=""
DRAWCOLOR="black"
BACKGROUNDCOLOR="white"
first= True
WOLINE=1
erased=[]

images=[]

icons=[]
class Example(Frame):
    
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    
        
    def initUI(self):
        
        def moveUp():
            w.tag_raise(images[WHICHIMAGE])
        def moveDown():
            w.tag_lower(images[WHICHIMAGE])
        def shrink():
            w.scale(images[WHICHIMAGE], 0, 0,1.1,1.1) 
        def increase():
            w.scale(images[WHICHIMAGE], 0,0, 0.5, 0.5) 
        def draw(event):
            global lastx
            global lasty
            lastx= lastx
            lasty=lasty
            if first:
                lastx=event.x
                lasty=event.y
                if WHATAMIDOING=="moving":
                    coords=[]
                    coords.append(lastx)
                    coords.append(lasty)
                    print images[WHICHIMAGE]
                    w.coords(images[WHICHIMAGE],lastx,lasty)
            else:
                if WHATAMIDOING==2:
                    global erased
                    era=w.create_line(lastx, lasty, event.x, event.y ,width=str(sp.get()), fill=DRAWCOLOR, tags="erased")
                    erased.append(era)
                elif WHATAMIDOING=="moving":
                    
                    w.coords(images[WHICHIMAGE],event.x, event.y )
                elif WHATAMIDOING==0:
                    w.create_line(lastx, lasty, event.x, event.y ,width=str(sp.get()), fill=DRAWCOLOR, tags="line")
                lastx=event.x
                lasty=event.y
            global first
            first = False  
        
        def reset(event):
            global first
            first = True
        
        
        def colorPick():
            color = askcolor() 
            global WHATAMIDOING
            
            if WHATAMIDOING == 3:
                global DRAWCOLOR
                DRAWCOLOR=color[1]
            else:
                global BACKGROUNDCOLOR
                BACKGROUNDCOLOR = color[1]
                w.configure(bg = BACKGROUNDCOLOR)
                for x in erased:
                    w.itemconfig(x,fill=BACKGROUNDCOLOR)

                print color
                
                
        def moveThis(x):
            global WHICHIMAGE
            WHICHIMAGE=x
            global WHATAMIDOING
            WHATAMIDOING="moving"
                          
        def changeEvent(event):
            global WHATAMIDOING
            WHATAMIDOING=event
            
            if WHATAMIDOING == 3 or WHATAMIDOING == 4  :
                colorPick()
                WHATAMIDOING=0
            
            elif WHATAMIDOING == 2 :
                global DRAWCOLOR
                DRAWCOLOR=BACKGROUNDCOLOR                    
                    
            elif WHATAMIDOING == 5 :
                global imageNew
                imageNew=askopenfilename(filetypes = [ ("Image Files", ("*.jpg", "*.gif","*.png")),("JPEG",'*.jpg'),("GIF",'*.gif'),('PNG','*.png') ] )
                
                global images 
                image = Image.open(imageNew)
                photo = ImageTk.PhotoImage(image)
                tag = "img"+str(len(images))
                w.create_image(0,0, image=photo, tags=tag)   
                icons.append(photo) # keep a reference! 
                resized =image.resize((50, 50))
                resized = ImageTk.PhotoImage(resized)
                global icons
                icons.append(resized)
                exitButton = Button(toolbar,image=resized, relief=FLAT, command= lambda x=len(images)-1 : moveThis(x))
                exitButton.pack(side=LEFT, padx=2, pady=2)
                images.append(tag)
                
                WHATAMIDOING=0
            print event
            
            
        self.parent.title("Toolbar")
        
        menubar = Menu(self.parent)
        self.fileMenu = Menu(self.parent, tearoff=0)
        self.fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=self.fileMenu)
        global w 
        w = Canvas(self.parent, bg=BACKGROUNDCOLOR)
        w.bind("<B1-Motion>", draw)
        w.bind("<ButtonRelease-1>", reset)
        w.pack(fill = BOTH, expand=True)  
        global toolbar
        toolbar = Frame(self.parent, bd=1, relief=RAISED)
        for x in range(6):
            
            exitButton = Button(toolbar, text=actionsarray[x], relief=FLAT, command= lambda x=x: changeEvent(x))
            exitButton.pack(side=LEFT, padx=2, pady=2)

        global sp   
        sp = Spinbox(toolbar, from_=1, to=30)
        sp.pack(side=LEFT, padx=2, pady=2)
        
        exitButton = Button(toolbar,text="Move Last Image to Front", relief=FLAT, command= moveUp)
        exitButton.pack(side=RIGHT, padx=2, pady=2)
        
        exitButton = Button(toolbar,text="Move Last Image to Back", relief=FLAT, command= moveDown)
        exitButton.pack(side=RIGHT, padx=2, pady=2)
        
        
        exitButton = Button(toolbar,text="Shrink Last Image", relief=FLAT, command= shrink)
        exitButton.pack(side=RIGHT, padx=2, pady=2)
        
        exitButton = Button(toolbar,text="Grow Last Image", relief=FLAT, command= increase)
        exitButton.pack(side=RIGHT, padx=2, pady=2)
        toolbar.pack(side = BOTTOM, fill=X)    
        self.parent.config(menu=menubar)
        self.pack()
        
       
    def onExit(self):
        self.quit()


def main():
  
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  