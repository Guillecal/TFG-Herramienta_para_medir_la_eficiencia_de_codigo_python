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
import tkFileDialog
import tkMessageBox
import ttk
import csv



import six
from matplotlib import animation
from matplotlib import style
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
        
        for F in (VentanaPrincipal, VentanaIndividual, VentanaAnalisis, VentanaMultiple, VentanaComparacion, VentanaComparacion2, VentanaParametros):
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
        """label = Tkinter.Label(self, text="Elige la opcion que desees:", font=LARGE_FONT)"""
        label = Tkinter.Label(self, text="Choose the option you want:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        """btn = Tkinter.Button(self, text="Analisis individual. Sin Parametros",command=lambda: controller.show_frame(VentanaIndividual))"""
        
        btn = Tkinter.Button(self, text="Individual analysis",command=lambda: controller.show_frame(VentanaIndividual))
        
        btn.pack()
        
        """btn2 = Tkinter.Button(self, text="Analisis Multifichero",command=lambda: controller.show_frame(VentanaMultiple))"""
        btn2 = Tkinter.Button(self, text="Comparative Analysis",command=lambda: controller.show_frame(VentanaMultiple))
        "Hacer una funcion que borre todos los frames"
        
        btn2.pack()
        
        """btn3 =Tkinter.Button(self, text="Analisis individual. Parametros",command=lambda: controller.show_frame(VentanaParametros))
        
        btn3.pack()"""
    

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
        """label = Tkinter.Label(self, text="Escoge el fichero a analizar:", font=LARGE_FONT)"""
        label = Tkinter.Label(self, text="Choose the file to analyze:", font=LARGE_FONT)
        
        label.pack(pady=10,padx=10)
        
        """btn2 = Tkinter.Button(self, text="Buscar fichero",command=self.V_analisis)"""
        btn2 = Tkinter.Button(self, text="Search file",command=self.V_analisis)
        
        btn2.pack()
        
        """btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))"""
        btn = Tkinter.Button(self, text="Return to the main screen",command=lambda: controller.show_frame(VentanaPrincipal))
        btn.pack()
        
    def V_analisis(self):
        self.nombre = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if self.nombre[len(self.nombre)-1]=="y" and self.nombre[len(self.nombre)-2]=="p" and self.nombre[len(self.nombre)-3]==".":
            "Se analiza cuando se  muestra el boton de Analizar fichero"
            self.pasa.frames[VentanaAnalisis].Analisis()
            
            if self.Boton1==0:
                print('hola')
                """btn3 = Tkinter.Button(self, text="Analizar fichero",command=lambda: self.pasa.show_frame(VentanaAnalisis))"""
                btn3 = Tkinter.Button(self, text="Analyze file",command=lambda: self.pasa.show_frame(VentanaAnalisis))
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
    ColoresF=['b','r','y','c','g','w','m','b','r','y','c','g','w','m','b','r','y','c','g','w','m']
        

    
    def __init__(self,parent,controller):
        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Analysis:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        """btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=lambda: controller.show_frame(VentanaPrincipal))"""
        btn = Tkinter.Button(self, text="Return to the main screen",command=lambda: controller.show_frame(VentanaPrincipal))
        btn.pack()
        
        """combo = ttk.Combobox(values=Procesadores.Archivos_csv)"""
        
        combo = ttk.Combobox(self, state="readonly")
        
        combo["values"] = Procesadores.Archivos_csv
        
        
        combo.set(Procesadores.Archivos_csv[0])
        
        combo.pack()
        
        self.Combo = combo
        
        

        """btn = Tkinter.Button(self, text="Mostrar Resultados",command=self.CambiaGrafico)"""
        btn = Tkinter.Button(self, text="Show results",command=self.CambiaGrafico)
        
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
                "Corregir"
                aux.append(a*int(Unidades[cont]))
                cont+=1
            
            print(aux)
            self.CiclosDeReloj[archivo]=aux

        "Recorre los tipos de operaciones y seleccionas los que luego deseas"
        for o in lab:
            self.VBoton.append(Tkinter.IntVar())
            Checkbutto.append(Tkinter.Checkbutton(self, text=o, variable=self.VBoton[enumera]))
            Checkbutto[enumera].pack(fill=Tkinter.BOTH, expand=1)
            Checkbutto[enumera].invoke()
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
            if op.get()==1:
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
                                if Fichero[linea][e]=='X':
                                    Unidades.append(1)
                                else:
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
        label = Tkinter.Label(self, text="Choose the files to analyze:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn2 = Tkinter.Button(self, text="Search files",command=self.V_analisis)
        
        btn2.pack()
        
        btn = Tkinter.Button(self, text="Return to the main screen",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
        
    def V_analisis(self):
        ArchivosCorrectos=0
        self.nombres = tkFileDialog.askopenfilenames(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        for comprobacion in self.nombres:
            if comprobacion[len(comprobacion)-1]!="y" or comprobacion[len(comprobacion)-2]!="p" and self.comprobacion[len(comprobacion)-3]!=".":
                ArchivosCorrectos=1
        
        if ArchivosCorrectos==1:
            tkMessageBox.showerror("Error","El fichero seleccionado no es de tipo .py")
        elif self.nombres.__len__()==1:
            tkMessageBox.showerror("Error","Solo has seleccionado 1 fichero")
        else:
            if self.nombres.__len__()<=10:
                if self.Boton1==0:
                    if self.Boton2==1:
                        btn3.pack_forget()
                    btn3 = Tkinter.Button(self, text="Comparison of files",command=lambda: self.pasa.show_frame(VentanaComparacion))
            
                    btn3.pack()
                    self.Boton1=1
                    self.Boton2=0
            else:
                if self.Boton2==0:
                    if self.Boton1==1:
                        btn3.pack_forget()
                    btn3 = Tkinter.Button(self, text="Comparison of files",command=lambda: self.pasa.show_frame(VentanaComparacion2))
            
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
            app.frames[VentanaComparacion2].Comba["values"] = self.OperacionesTotales

        
            "app.frames[VentanaComparacion].Comba.pack()"
            app.frames[VentanaComparacion].btn2.pack()
            "app.frames[VentanaComparacion2].Comba.pack()"
            app.frames[VentanaComparacion2].btn2.pack()
            app.frames[VentanaComparacion].Muestra_Botones()
            app.frames[VentanaComparacion2].Muestra_Botones()
            
            for marcar in range(0,app.frames[VentanaComparacion].VBoton.__len__()):
                app.frames[VentanaComparacion].Checkbutto[marcar].invoke()
                app.frames[VentanaComparacion2].Checkbutto[marcar].invoke()
        
        
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
                                if Fichero[linea][e]=='X':
                                    Unidades.append(1)
                                else:
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
    alfabeto=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','aa','ab','ac','ad']
    VBoton=[] 
    Checkbutto=[]
    Combo=[]
    Comba=[]
    Fichero=[]
    Valor_Mostrar=[]
    Nombre=[]
    Muestrafichero=0
    ValoresTotales=[]
    
    def __init__(self,parent,controller):
        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Comparison:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn = Tkinter.Button(self, text="Return to the main screen",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
        
        """combo = ttk.Combobox(values=Procesadores.Archivos_csv)"""
        
        combo = ttk.Combobox(self, state="readonly")
        
        combo["values"] = Procesadores.Archivos_csv
        
        
        
        combo.pack()
        
        self.Combo = combo
        
        
        comba = ttk.Combobox(self, state="readonly")
        
        self.Comba = comba
        
        
        btn2 = Tkinter.Button(self, text="Show results",command=self.Sacar_Valores)
        
        self.btn2=btn2
        
        self.canvas = FigureCanvasTkAgg(f2, self)
        
        
    def Muestra_Botones(self):
        enumera=0
        for o in app.frames[VentanaMultiple].OperacionesTotales:
            self.VBoton.append(Tkinter.IntVar())
            self.Checkbutto.append(Tkinter.Checkbutton(self, text=o, variable=self.VBoton[enumera]))
            self.Checkbutto[enumera].pack(fill=Tkinter.BOTH, expand=1)
            "self.canvas.create_window(85, posi, window=Checkbutto[enumera])"
            enumera=enumera+1
        
        
    def Sacar_Valores(self):
       
        contador=1
        pasa=0
        self.Fichero=[]
        self.Nombre=[]
        self.Valor_Mostrar=[]
        contador_menor=0
        "igual hay que  cambiar este bucle, por otro de nombres (en principio el resultado es el mismo)"
        for e in app.frames[VentanaMultiple].Operaciones:
            self.Fichero.append(self.alfabeto[contador_menor])
            self.Valor_Mostrar.append(0)
            contador_menor=contador_menor+1
        contador_operaciones=0
        for Ototal in app.frames[VentanaMultiple].OperacionesTotales:
            if self.VBoton[contador_operaciones].get()==1:
                contador_menor=0
                for Omenor in app.frames[VentanaMultiple].Operaciones.values():
                    cont_interior=0
                    for i in Omenor:
                        print(Ototal)
                        print(i)
                        if Ototal==i:
                            self.Valor_Mostrar[contador_menor]=app.frames[VentanaMultiple].CiclosDeReloj[contador_menor+1][self.Combo.get()][cont_interior]+self.Valor_Mostrar[contador_menor]
                        cont_interior=cont_interior+1
                    contador_menor=contador_menor+1
            contador_operaciones=contador_operaciones+1
        """for cosa in app.frames[VentanaMultiple].nombres:
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
            contador=contador+1"""
        print(self.Fichero)
        print(self.Valor_Mostrar)
        print('hola')
        print(self.VBoton[0])

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
    alfabeto=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','aa','ab','ac','ad']
    VBoton=[] 
    Checkbutto=[]
    Combo=[]
    Comba=[]
    Fichero=[]
    Valor_Mostrar=[]
    Nombre=[]
    Muestrafichero=0
    ValoresTotales=[]
    Entry=None
    Entry2=None
    btn3=None

    def __init__(self,parent,controller):

        self.Pasadita=parent
        self.pasa=controller
        
        Tkinter.Frame.__init__(self,parent)
        label = Tkinter.Label(self, text="Comparison:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        btn = Tkinter.Button(self, text="Return to the main screen",command=lambda: controller.show_frame(VentanaPrincipal))
        
        btn.pack()
        
        
        """combo = ttk.Combobox(values=Procesadores.Archivos_csv)"""
        
        combo = ttk.Combobox(self, state="readonly")
        
        combo["values"] = Procesadores.Archivos_csv
        
        
        
        combo.pack()
        
        self.Combo = combo
        
        
        comba = ttk.Combobox(self, state="readonly")
        
        self.Comba = comba
        
        
        btn2 = Tkinter.Button(self, text="Show results",command=self.Sacar_Valores)
        
        self.btn2=btn2
        
        self.canvas = FigureCanvasTkAgg(f3, self)
   

    def Muestra_Botones(self):
        enumera=0
        for o in app.frames[VentanaMultiple].OperacionesTotales:
            self.VBoton.append(Tkinter.IntVar())
            self.Checkbutto.append(Tkinter.Checkbutton(self, text=o, variable=self.VBoton[enumera]))
            self.Checkbutto[enumera].pack(fill=Tkinter.BOTH, expand=1)
            "self.canvas.create_window(85, posi, window=Checkbutto[enumera])"
            enumera=enumera+1     
        
    def Sacar_Valores(self):
       
        
        contador=1
        pasa=0
        self.Fichero=[]
        self.Nombre=[]
        self.Valor_Mostrar=[]
        contador_menor=0
        "igual hay que  cambiar este bucle, por otro de nombres (en principio el resultado es el mismo)"
        for e in app.frames[VentanaMultiple].Operaciones:
            self.Fichero.append(self.alfabeto[contador_menor])
            self.Valor_Mostrar.append(0)
            contador_menor=contador_menor+1
        contador_operaciones=0
        for Ototal in app.frames[VentanaMultiple].OperacionesTotales:
            if self.VBoton[contador_operaciones].get()==1:
                contador_menor=0
                for Omenor in app.frames[VentanaMultiple].Operaciones.values():
                    cont_interior=0
                    for i in Omenor:
                        print(Ototal)
                        print(i)
                        if Ototal==i:
                            self.Valor_Mostrar[contador_menor]=app.frames[VentanaMultiple].CiclosDeReloj[contador_menor+1][self.Combo.get()][cont_interior]+self.Valor_Mostrar[contador_menor]
                        cont_interior=cont_interior+1
                    contador_menor=contador_menor+1
            contador_operaciones=contador_operaciones+1
        """contador=1
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
        print(self.Valor_Mostrar)"""
        if self.Muestrafichero==0:
            print("holo")
            self.Muestrafichero=1
            label = Tkinter.Label(self, text="Introduce un ID:")
            label.pack();
            self.Entry=Tkinter.Entry(self)
        
            self.Entry.pack()
            
            self.btn3 = Tkinter.Button(self, text="Find Name",command=self.Saca_Nombre)
            
            self.btn3.pack()
            
            self.Entry2=Tkinter.Entry(self)
            
            self.Entry2.pack()
            
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=Tkinter.BOTTOM, fill=Tkinter.BOTH, expand=True)
                
            toolbar= NavigationToolbar2Tk(self.canvas, self)
            toolbar.update()
            self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=True)
            
            
        
            """btn = Tkinter.Button(self, text="Volver a la pantalla principal",command=MuestraNombre)
        
            btn.pack()"""
    
    """def MuestraNombre(self):
        contador=0
        for i in self.alfabeto:
            if i==self.Entry.get():
                self.Entry2(0,self.Nombre[contador])"""
    
    def Saca_Nombre(self):
        contador=0
        longi=0
        caracter=None
        for a in self.Fichero:
            if a==self.Entry.get():
                self.Entry2.delete(0,Tkinter.END)
                longi=app.frames[VentanaMultiple].nombres[contador].__len__()
                for c in range(longi):
                    if app.frames[VentanaMultiple].nombres[contador][longi-c-1]=="/":
                        caracter=longi-c
                        self.Entry2.insert(0,app.frames[VentanaMultiple].nombres[contador][caracter:longi])
                        break
            contador=contador+1    
        if caracter==None:
            self.Entry2.delete(0,Tkinter.END)
            self.Entry2.insert(0,"No Existe")
        
        
        
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

class VentanaParametros(Tkinter.Frame):
    nombre=None
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
        self.nombre = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if self.nombre[len(self.nombre)-1]=="y" and self.nombre[len(self.nombre)-2]=="p" and self.nombre[len(self.nombre)-3]==".":
            "Se analiza cuando se  muestra el boton de Analizar fichero"
            "self.pasa.frames[VentanaAnalisis].Analisis()"
            if self.Boton1==0:
                btn3 = Tkinter.Button(self, text="Analizar fichero",command=print("hola"))
                btn3.pack()
                self.Boton1=1
            
        else:
            tkMessageBox.showerror("Error","El fichero seleccionado no es de tipo .py")
            
        tkMessageBox.showerror("Error","Se esta trabajando en esta nueva funcionalidad")
    
    

    
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
    a3.plot(app.frames[VentanaComparacion2].Fichero,app.frames[VentanaComparacion2].Valor_Mostrar, 'ro-')
    """(app.frames[VentanaComparacion].Fichero,app.frames[VentanaComparacion].Valor_Mostrar,align="center")"""
    
    
ani = animation.FuncAnimation(f, animate, interval=1000)
ani2= animation.FuncAnimation(f2, animate2, interval=1000)
ani3= animation.FuncAnimation(f3, animate3, interval=1000)
app.mainloop()