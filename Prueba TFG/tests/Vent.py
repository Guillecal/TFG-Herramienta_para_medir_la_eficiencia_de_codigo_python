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
import numpy


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
f2 = Figure(figsize=(5,5), dpi=100)
a2 = f2.add_subplot(111)
f3 = Figure(figsize=(5,5), dpi=100)
a3 = f3.add_subplot(111)


class SeaofBTCapp(Tkinter.Tk):
    
    def __init__(self, *args, **kwargs):
        Tkinter.Tk.__init__(self, *args, **kwargs)
        container = Tkinter.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        for F in (VentanaPrincipal, VentanaIndividual, VentanaAnalisis, VentanaMultiple, VentanaComparacion, VentanaComparacion2):
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
    Boton1=0
    
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
            if self.Boton1==0:
                btn3 = Tkinter.Button(self, text="Analizar fichero",command=lambda: self.pasa.show_frame(VentanaAnalisis))
                btn3.pack()
                self.Boton1=1
            
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
    CiclosDeReloj={}
    Archivos_pro=[]
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
        for archivo in Procesadores.Archivos_csv:
            Unidades=self.SacarCiclosDeReloj(archivo,vm.opera.keys())
            aux=[]
            cont=0
            print(Unidades)
            for a in self.ValoresF:
                print(a)
                aux.append(a*int(Unidades[cont]))
                cont+=1
            
            print(aux)
            self.CiclosDeReloj[archivo]=aux

        "Recorre los tipos de operaciones y seleccionas los que luego deseas"
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
                NewValores.append(self.CiclosDeReloj[self.Combo.get()][num])
            num+=1
        if NewOperadores.__len__==0:
            self.Operaciones=self.OperacionesF
            self.Valores=self.CiclosDeReloj[self.Combo.get()]
            self.Colores=self.ColoresF
            tkMessageBox.showerror("Error","No puedes quitar todas las operaciones .py")
        else:
            self.Operaciones=NewOperadores
            self.Valores=NewValores
            self.Colores=NewColores
        print(self.Operaciones)
        print(self.Valores)
        print(self.Colores)
            
    def SacarCiclosDeReloj(self,Proce,Operadores):
        Fichero=[]
        Unidades=[]
        UnidadesF=[]
        Flag=[]
        """cambiar ruta"""
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
    Boton2=0
    Boton1=0
    cont=0
    Pasadita=None
    pasa=None
    Value={}
    Operaciones={}
    CiclosDeReloj={}
    OperacionesTotales=[]
    
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
        ArchivosCorrectos=0
        self.nombres = tkFileDialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        for comprobacion in self.nombres:
            if comprobacion[len(comprobacion)-1]!="y" or comprobacion[len(comprobacion)-2]!="p" and self.comprobacion[len(comprobacion)-3]!=".":
                ArchivosCorrectos=1
        
        if ArchivosCorrectos==1:
            tkMessageBox.showerror("Error","El fichero seleccionado no es de tipo .py")
        else:
            if self.nombres.__len__()<=10:
                if self.Boton1==0:
                    if self.Boton2==1:
                        btn3.pack_forget()
                    btn3 = Tkinter.Button(self, text="Comparacion de ficheros",command=lambda: self.pasa.show_frame(VentanaComparacion))
            
                    btn3.pack()
                    self.Boton1=1
                    self.Boton2=0
            else:
                if self.Boton2==0:
                    if self.Boton1==1:
                        btn3.pack_forget()
                    btn3 = Tkinter.Button(self, text="Comparacion de ficheros",command=lambda: self.pasa.show_frame(VentanaComparacion2))
            
                    btn3.pack()
                    self.Boton1=1
                    self.Boton2=0
                
            Checkbutto=[]
            Unidades=[]
            posi=190
            enumera=1
            
            for ficherin in self.nombres:
                lab=[]
                CiclosDeReloj_dentro={}
                f = open (ficherin,'r')
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
                self.Operaciones[enumera]=lab
                "self.OperacionesF=lab"
                self.Value[enumera]=vm.opera.values()
                "self.ValoresF=vm.opera.values()"
                for oper in lab:
                    if oper not in self.OperacionesTotales:
                        self.OperacionesTotales.append(oper)
                
                for archivo in Procesadores.Archivos_csv:
                    Unidades=self.SacarCiclosDeReloj(archivo,vm.opera.keys())
                    aux=[]
                    cont=0
                    print(Unidades)
                    for a in self.Value[enumera]:
                        print(a)
                        aux.append(a*int(Unidades[cont]))
                        cont+=1
                    
                    print(aux)
                    CiclosDeReloj_dentro[archivo]=aux
                self.CiclosDeReloj[enumera]=CiclosDeReloj_dentro
                enumera=enumera+1
            print(self.CiclosDeReloj)
            print(self.OperacionesTotales)
            print(self.Operaciones)
            app.frames[VentanaComparacion].Comba["values"] = self.OperacionesTotales

        
            app.frames[VentanaComparacion].Comba.pack()
            app.frames[VentanaComparacion].btn2.pack()
    
        
    def SacarCiclosDeReloj(self,Proce,Operadores):
        Fichero=[]
        Unidades=[]
        Flag=[]
        """cambiar ruta"""
        archivo = open('C:/Users/Adrian/Documents/GitHub/TFG-Herramienta_para_medir_la_eficiencia_de_codigo_python/Prueba TFG/tests/'+Proce)
        Lectura = csv.reader(archivo,delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)

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
    
    
class VentanaComparacion(Tkinter.Frame):
    
    Pasadita=None
    pasa=None
    btn2=None
    VBoton=[] 
    Combo=[]
    Comba=[]
    Fichero=[]
    Valor_Mostrar=[]
    Nombre=[]
    Muestrafichero=0
    
    def __init__(self,parent,controller):
        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Comparacion:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
        
        """combo = ttk.Combobox(values=Procesadores.Archivos_csv)"""
        
        combo = ttk.Combobox(self, state="readonly")
        
        combo["values"] = Procesadores.Archivos_csv
        
        
        
        combo.pack()
        
        self.Combo = combo
        
        
        comba = ttk.Combobox(self, state="readonly")
        
        self.Comba = comba
        
        
        btn2 = Tkinter.Button(self, text="Mostrar Analisis",command=self.Sacar_Valores)
        
        self.btn2=btn2
        
        self.canvas = FigureCanvasTkAgg(f2, self)
        
        
        
    def Sacar_Valores(self):
       
        contador=1
        pasa=0
        self.Fichero=[]
        self.Nombre=[]
        self.Valor_Mostrar=[]
        for cosa in app.frames[VentanaMultiple].nombres:
            Op=0
            for a in app.frames[VentanaMultiple].Operaciones[contador]:
                if a == self.Comba.get():
                    pasa=1
                if pasa==1:
                    self.Fichero.append(contador)
                    "Mirar como solo obtener el nombre"
                    self.Nombre.append(app.frames[VentanaMultiple].nombres[contador-1])
                    self.Valor_Mostrar.append(app.frames[VentanaMultiple].CiclosDeReloj[contador][self.Combo.get()][Op])
                    pasa=0
                Op=Op+1
            contador=contador+1
        print(self.Fichero)
        print(self.Valor_Mostrar)

        if self.Muestrafichero==0:
            print("hola")
            self.Muestrafichero=1
            print(self.Muestrafichero)
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)
            
            toolbar= NavigationToolbar2Tk(self.canvas, self)
            toolbar.update()
            self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=True)
            

        
class VentanaComparacion2(Tkinter.Frame):
    
    Pasadita=None
    pasa=None
    btn2=None
    VBoton=[] 
    Combo=[]
    Comba=[]
    Fichero=[]
    Valor_Mostrar=[]
    Muestrafichero=0


    def __init__(self,parent,controller):
        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Comparacion:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
        
        """combo = ttk.Combobox(values=Procesadores.Archivos_csv)"""
        
        combo = ttk.Combobox(self, state="readonly")
        
        combo["values"] = Procesadores.Archivos_csv
        
        
        
        combo.pack()
        
        self.Combo = combo
        
        
        comba = ttk.Combobox(self, state="readonly")
        
        self.Comba = comba
        
        
        btn2 = Tkinter.Button(self, text="Mostrar Analisis",command=self.Sacar_Valores)
        
        self.btn2=btn2
        
        self.canvas = FigureCanvasTkAgg(f3, self)
        
        
    def Sacar_Valores(self):
       
        contador=1
        pasa=0
        self.Fichero=[]
        self.Valor_Mostrar=[]
        for cosa in app.frames[VentanaMultiple].nombres:
            Op=0
            for a in app.frames[VentanaMultiple].Operaciones[contador]:
                if a == self.Comba.get():
                    pasa=1
                if pasa==1:
                    self.Fichero.append(contador)
                    self.Valor_Mostrar.append(app.frames[VentanaMultiple].CiclosDeReloj[contador][self.Combo.get()][Op])
                    pasa=0
                Op=Op+1
            contador=contador+1
        print(self.Fichero)
        print(self.Valor_Mostrar)
        if self.Muestrafichero==0:
            self.MuestraFichero=1
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)
                
            toolbar= NavigationToolbar2Tk(self.canvas, self)
            toolbar.update()
            self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=True)
            

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
    "a.title(app.frames[VentanaAnalisis].Combo.get())"
    
def animate2(self):
    
    a2.clear()
    a2.bar(app.frames[VentanaComparacion].Fichero,app.frames[VentanaComparacion].Valor_Mostrar,align="center")
    
def animate3(self):
    
    a3.clear()
    a3.bar(app.frames[VentanaComparacion].Fichero,app.frames[VentanaComparacion].Valor_Mostrar,align="center")
    
    
ani = animation.FuncAnimation(f, animate, interval=1000)
ani2= animation.FuncAnimation(f2, animate2, interval=1000)
ani3= animation.FuncAnimation(f3, animate3, interval=1000)
app.mainloop()