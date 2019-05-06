"""Testing tools for byterun."""

from __future__ import print_function

import matplotlib.pyplot as plt
import os
import Tkinter
import dis
import sys
import textwrap
import types
import unittest
import Tkconstants, tkFileDialog

import six
from pandas import DataFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from byterun.pyvm2 import VirtualMachine, VirtualMachineError




def dis_code(code):
    """Disassemble `code` and all the code it refers to."""
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            dis_code(const)

    print("")
    print(code)
    dis.dis(code)

# Make this false if you need to run the debugger inside a test.
"CAPTURE_STDOUT = ('-s' not in sys.argv)"
# Make this false to see the traceback from a failure inside pyvm2.

"--------------------------------------------------------------------"


class windows(object):
    top = Tkinter.Tk()
    canvas1 = Tkinter.Canvas(top, width = 800, height = 350) 
    canvas1.pack()
    "top.geometry('350x200')"
    top.title("Analisis de codigo Python")
    lbl = Tkinter.Label(top, text="Que fichero deseas analizar:")
    canvas1.create_window(140, 40, window=lbl)
    "lbl.grid(column=0, row=0)"
    txt = Tkinter.Entry(top,width=22)
    canvas1.create_window(140, 60, window=txt)
    "txt.grid(column=1, row=0)"
    Archivos=[]
    Archivos_py=[]
    key=[]
    key_string=[]
    value=[]
    dic2={}
    Dic_Conjunto={}
    Dic_posicion={}
        
    
    def seleccionar_ficheros(self):
        self.top.filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        print (self.top.filename)
        
        
        
        
    def clicked(self):
        self.Archivos=os.listdir(self.txt.get())
        for i in self.Archivos:
            if i[len(i)-1]=="y" and i[len(i)-2]=="p" and i[len(i)-3]==".":
                print("Pasaste la prueba")
                self.Archivos_py.append(i)
            else:
                print("A tu casa")
        
        print(self.Archivos_py)
        cont=1
        for i in self.Archivos_py:
            f = open (self.txt.get()+'\\' +i,'r')
            mensaje = f.read()
            print(mensaje)
    
            CAPTURE_EXCEPTION = 1
    
    
            code=mensaje
            f.close()
    
            code = textwrap.dedent(code)
            code = compile(code, "<%s>" % id(code), "exec", 0, 1)
            dis_code(code)
            vm_stdout = six.StringIO()
            vm = VirtualMachine()
            vm_value = self.vm_exc = None
            vm_value = vm.run_code(code)
            self.key=vm.opera.keys()
            self.value=vm.opera.values()
            print(self.key)
            print(self.value)
            self.dic2['tipos']=self.key
            self.dic2['contoladores']=self.value
            print(self.key)
            print(self.value)
            self.key_string=[]
            
            "---------------------------------------------------------------------------------"         
            df1 = DataFrame(self.dic2,columns=['tipos','contoladores'])
            "print(df1)"
            "df1 = DataFrame(vm.opera, c=vm.opera.keys())"
            
            "root= Tkinter.Tk()"            
            figure1 = plt.Figure(figsize=(6,5), dpi=100)
            ax1 = figure1.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure1, self.top)
            bar1.get_tk_widget().pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
            "df1.plot(kind='bar', legend=True, ax=ax1)"
            for e in self.key:
                self.key_string.append(e[0])
            ax1.bar( self.key_string,self.value, color = 'g')
            bar1 = FigureCanvasTkAgg(figure1, self.top) # create a canvas figure (matplotlib module)
            bar1.get_tk_widget().pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, expand=0)
            ax1.set_title(i)
            stringu=''
            conta_pos=0
            for x in vm.opera.keys():
                stringu=stringu+str(x[0])+': '+str(vm.opera[x])+'('+str(x[1])[7:10]+', '+str(x[2])[7:10]+')'+'\n'
                conta_pos+=5
            self.Dic_Conjunto[cont]=stringu
            self.Dic_posicion[cont]=conta_pos
            cont+=1
            "------------------------------------------------------------------------------------"            
     
        self.lbl.configure(text="Button was clicked !!")
        cont_lineas=2
        cont_dic=1
        posicion=20
        for i in self.Archivos_py:
            lbl2 = Tkinter.Label(self.top, text="Las operaciones del archivo "+i+" son:")
            "lbl2.grid(column=0, row=cont_lineas)"
            self.canvas1.create_window(500, posicion, window=lbl2)
            posicion+=30+self.Dic_posicion[cont_dic]
            cont_lineas+=1
            stringu=self.Dic_Conjunto[cont_dic]
            lbl3 = Tkinter.Label(self.top, text=stringu)
            "lbl3.grid(column=1, row=cont_lineas)"
            self.canvas1.create_window(500, posicion, window=lbl3)
            posicion+=30+(self.Dic_posicion[cont_dic])
            cont_dic+=1
            cont_lineas+=1
            
    

w=windows()
btn = Tkinter.Button(w.top, text="Click Me",command=w.clicked)
w.canvas1.create_window(97, 110, window=btn)


 
"""btn.grid(column=2, row=0)"""
# creating a button instance
quitButton = Tkinter.Button(w.top,text="Quit",command=w.top.destroy)
w.canvas1.create_window(85, 140, window=quitButton)

        # placing the button on my window
"""quitButton.grid(column=4, row=0)"""
# Code to add widgets will go here...
w.top.mainloop()

