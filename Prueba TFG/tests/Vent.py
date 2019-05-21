# -*- coding: utf-8 -*-
"""
Created on Sat May  4 12:07:45 2019

@author: Adrian
"""

from __future__ import print_function
import matplotlib 
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,    NavigationToolbar2Tk
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
import ttk
import csv


import six
from matplotlib import animation
from matplotlib import style
from pandas import DataFrame
from matplotlib.figure import Figure


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
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


class SeaofBTCapp(Tkinter.Tk):
    
    def __init__(self, *args, **kwargs):
        Tkinter.Tk.__init__(self, *args, **kwargs)
        container = Tkinter.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        for F in (VentanaPrincipal, VentanaIndividual, VentanaAnalisis, VentanaMultiple):
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
        
        btn2 = Tkinter.Button(self, text="Analisis Multifichero",command=lambda: controller.show_frame(VentanaMultiple))
        "Hacer una funcion que borre todos los frames"
        
        btn2.pack()
    

class VentanaIndividual(Tkinter.Frame):
    
    nombre=""
    cont=0
    Pasadita=None
    pasa=None
    
    def __init__(self,parent,controller):
        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Escoge el fichero a analizar:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn2 = Tkinter.Button(self, text="Buscar fichero",command=self.V_analisis)
        
        btn2.pack()
        
        btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
    def V_analisis(self):
        self.nombre = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if self.nombre[len(self.nombre)-1]=="y" and self.nombre[len(self.nombre)-2]=="p" and self.nombre[len(self.nombre)-3]==".":
            "Se analiza cuando se  muestra el boton de Analizar fichero"
            self.pasa.frames[VentanaAnalisis].Analisis()
            btn3 = Tkinter.Button(self, text="Analizar fichero",command=lambda: self.pasa.show_frame(VentanaAnalisis))
            btn3.pack()
            
        else:
            tkMessageBox.showerror("Error","El fichero seleccionado no es de tipo .py")
        
        
class VentanaAnalisis(Tkinter.Frame):
    
    Pasadita=None
    pasa=None
    canva=None
    bar1=None
    xList =[]
    yList =[]
    Operaciones=[]
    OperacionesF=[]
    Valores=[]
    ValoresF=[]
    VBoton=[]
    Colores=[]
    Combo=[]
    CiclosDeReloj=[]
    ColoresF=['b','r','y','c','g']
        

    
    def __init__(self,parent,controller):
        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Analisis:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
        """combo = ttk.Combobox(values=Procesadores.Archivos_csv)"""
        
        combo = ttk.Combobox(self, state="readonly")
        
        combo["values"] = Procesadores.Archivos_csv
        
        combo.set(Procesadores.Archivos_csv[0])
        
        combo.pack()
        
        self.Combo = combo
        
        

        btn = Tkinter.Button(self, text="Ordenar Operaciones",command=self.CambiaGrafico)
        
        btn.pack()
        
        self.canvas = FigureCanvasTkAgg(f, self)
        
    
    def Analisis(self):
        print("hola")
        lab=[]
        Checkbutto=[]
        Unidades=[]
        posi=190
        enumera=0
        f = open (self.pasa.frames[VentanaIndividual].nombre,'r')
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
        
        labels=lab
        self.Operaciones=lab
        self.OperacionesF=lab
        self.Valores=vm.opera.values()
        self.ValoresF=vm.opera.values()
        values=vm.opera.values()
        self.xList=[1,2,3,4,5]
        self.yList=values
        Unidades=self.SacarCiclosDeReloj(self.Combo.get(),vm.opera.keys())
        aux=[]
        cont=0
        for a in self.ValoresF:
            aux.append(a*Unidades[cont])
        self.CiclosDeReloj=aux

        "Recorre los tipos de operaaciones y seleccionas los que luego deseas"
        for o in lab:
            self.VBoton.append(Tkinter.IntVar())
            Checkbutto.append(Tkinter.Checkbutton(self, text=o, variable=self.VBoton[enumera]))
            Checkbutto[enumera].pack(fill=Tkinter.BOTH, expand=1)
            self.Colores.append(self.ColoresF[enumera])
            "self.canvas.create_window(85, posi, window=Checkbutto[enumera])"
            posi=posi+20
            enumera=enumera+1
        print(self.VBoton)
        
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)
        
        toolbar= NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=True)
        
        """
        figure1 = plt.Figure(figsize=(6,5), dpi=100)
        labels=lab
        values=vm.opera.values()
        explode=[0,0,0,0.05,0]
        colors=["c","b","g","r","y"]
        plt.pie(values,labels=labels,autopct="%.f%%",explode=explode,colors=colors)
        bar1 = FigureCanvasTkAgg(figure1, self.top)
        bar1.get_tk_widget().pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)"""
        
    def CambiaGrafico(self):
        num=0
        NewOperadores=[]
        NewValores=[]
        NewColores=[]
        for op in self.VBoton:
            if op.get()==0:
                NewColores.append(self.ColoresF[num])
                NewOperadores.append(self.OperacionesF[num])
                NewValores.append(self.ValoresF[num])
            num+=1
        if NewOperadores.__len__==0:
            self.Operaciones=self.OperacionesF
            self.Valores=self.elf.ValoresF
            self.Colores=self.ColoresF
            tkMessageBox.showerror("Error","No puedes quitar todas las operaciones .py")
        else:
            self.Operaciones=NewOperadores
            self.Valores=NewValores
            self.Colores=NewColores
            
    def SacarCiclosDeReloj(self,Proce,Operadores):
        Fichero=[]
        Unidades=[]
        Flag=[]
        paso=0
        archivo = open('C:/Users/Adrian/Documents/GitHub/TFG-Herramienta_para_medir_la_eficiencia_de_codigo_python/Prueba TFG/tests/'+Proce)
        Lectura = csv.reader(archivo,delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
        self.ValoresF
        self.OperacionesF
        print(Operadores)
        for x in Lectura:
            Fichero.append(x)
        
        for Opera in range(0,Operadores.__len__()):
            Flag.append(0)
            for linea in range(0,Fichero.__len__()):
                if Fichero[linea][0]==Operadores[Opera][0]:
                    if Fichero[linea][1]==str(Operadores[Opera][1])[7:10]:
                        for e in range(2,7):
                            if Fichero[0][e]==str(Operadores[Opera][2])[7:10]:
                                Unidades.append(Fichero[linea][e])
                                Flag[Opera]=1
            "Esto pasa por tener mal ajustado el procesador"
            if Flag[Opera]==0:
                Flag[Opera]=1
                Unidades.append(1)
        print(Unidades)
        return Unidades            
        
        
class VentanaMultiple(Tkinter.Frame):
    
    nombres=[]
    cont=0
    Pasadita=None
    pasa=None
    
    def __init__(self,parent,controller):
        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Escoge el fichero a analizar:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn2 = Tkinter.Button(self, text="Buscar fichero",command=self.V_analisis)
        
        btn2.pack()
        
        btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
    
    def V_analisis(self):
        self.nombres = tkFileDialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        tkMessageBox.showerror("Error","Se esta trabajando en ello")

class RecogeDatos():
    direccion='C:/Users/Adrian/Documents/GitHub/TFG-Herramienta_para_medir_la_eficiencia_de_codigo_python/Prueba TFG/tests'
    Archivos=[]
    Archivos_csv=[]
    
    def __init__(self):
        
        self.Archivos=os.listdir(self.direccion)
        for i in self.Archivos:
            if i[len(i)-1]=="v" and i[len(i)-2]=="s" and i[len(i)-3]=="c" and i[len(i)-4]=='.':
                self.Archivos_csv.append(i)
        print(self.Archivos_csv)

Procesadores=RecogeDatos()
app=SeaofBTCapp()

def animate(self):
    
        a.clear()
        a.pie(app.frames[VentanaAnalisis].Valores, labels=app.frames[VentanaAnalisis].Operaciones,colors=app.frames[VentanaAnalisis].Colores, startangle=90, autopct='%.1f%%')
        
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()