import Tkinter

top = Tkinter.Tk()
top.geometry('350x200')
top.title("Welcome to LikeGeeks app")
lbl = Tkinter.Label(top, text="Hello")
 
lbl.grid(column=0, row=0)
txt = Tkinter.Entry(top,width=10)
txt.grid(column=1, row=0)

def clicked():
 
    lbl.configure(text="Button was clicked !!")

btn = Tkinter.Button(top, text="Click Me",command=clicked)



 
btn.grid(column=2, row=0)
# Code to add widgets will go here...
top.mainloop()