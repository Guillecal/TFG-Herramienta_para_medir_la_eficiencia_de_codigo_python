# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:07:45 2019

@author: Adrian
"""

from __future__ import print_function
import matplotlib 
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
import os
import Tkinter
import dis
import sys
import textwrap
import types
import unittest
import Tkconstants, tkFileDialog
import tkMessageBox


import six
from pandas import DataFrame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

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
LARGE_FONT= ("Verdana", 12)

class SeaofBTCapp(Tkinter.Tk):
    
    def __init__(self, *args, **kwargs):
        Tkinter.Tk.__init__(self, *args, **kwargs)
        container = Tkinter.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (VentanaPrincipal, VentanaIndividual):
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(VentanaPrincipal)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
    
    
class VentanaPrincipal(Tkinter.Frame):
    
    def __init__(self,parent,controller):
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Elige la opcion que desees:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn = Tkinter.Button(self, text="Analisis individual",command=lambda: controller.show_frame(VentanaIndividual))
        
        btn.pack()
        
        btn2 = Tkinter.Button(self, text="Analisis Multifichero",command=self.destroy)
        "Hacer una funcion que borre todos los frames"
        
        btn2.pack()
    

class VentanaIndividual(Tkinter.Frame):
    
    N_fichero=""
    
    def __init__(self,parent,controller):
        Tkinter.Frame.__init__(self,parent)
        fiche=fichero()
        label = Tkinter.Label(self, text="Escoge el fichero a analizar:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn2 = Tkinter.Button(self, text="Buscar fichero",command=fiche.pulsar)
        
        btn2.pack()
        
        btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
        self.N_fichero=fiche.nombre
        
    def analisis(N_fichero):
        lab=[]
        Checkbutto=[]
        var=[]
        posi=190
        enumera=0
        f = open (f,'r')
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
        for i in vm.opera.keys():
            lab.append(i[0]+"_"+str(i[1])[7:10]+"_"+str(i[2])[7:10])
        
        
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        labels=lab
        values=vm.opera.values()
        explode=[0,0,0,0.05,0]
        colors=["c","b","g","r","y"]
        plt.pie(values,labels=labels,autopct="%.f%%",explode=explode,colors=colors)
        bar1 = FigureCanvasTkAgg(figure1, self.top)
        bar1.get_tk_widget().pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
    
class fichero(Tkinter.Tk):
    
    nombre=""
    

    def pulsar(self):
        self.nombre = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        print (self.nombre)
        if self.nombre[len(self.nombre)-1]=="y" and self.nombre[len(self.nombre)-2]=="p" and self.nombre[len(self.nombre)-3]==".":
            tkMessageBox.showerror("Lets go","El fichero seleccionado si es de tipo .py")
            btn3 = Tkinter.Button(self, text="Analizar: "+self.nombre,command=lambda: controller.show_frame(VentanaIndividual))
        
            btn3.pack()
        else:
            tkMessageBox.showerror("Error","El fichero seleccionado no es de tipo .py")
            
    
app=SeaofBTCapp()
app.mainloop()