import Tkinter

top = Tkinter.Tk()
top.geometry('350x200')
top.title("Welcome to LikeGeeks app")
lbl = Tkinter.Label(top, text="Hello")
 
lbl.grid(column=0, row=0)
txt = Tkinter.Entry(top,width=10)
txt.grid(column=1, row=0)

def client_exit():
    exit()
        
def clicked():
 
    lbl.configure(text="Button was clicked !!")

btn = Tkinter.Button(top, text="Click Me",command=clicked)
quitButton = Tkinter.Button(top,text="Quit",command=client_exit)

        # placing the button on my window
quitButton.grid(column=4, row=0)


 
btn.grid(column=2, row=0)
# Code to add widgets will go here...
top.mainloop()