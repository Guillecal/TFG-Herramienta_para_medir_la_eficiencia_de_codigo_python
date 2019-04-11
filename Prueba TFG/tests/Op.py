"""Testing tools for byterun."""

from __future__ import print_function

import Tkinter
import dis
import sys
import textwrap
import types
import unittest

import six

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
    respuesta = input("¿Deseas (1) analizar un codigo o (2) comparar dos codigos? ")
    top = Tkinter.Tk()
    top.geometry('350x200')
    top.title("Analisis de codigo Python")
    lbl = Tkinter.Label(top, text="¿Que fichero deseas analizar?")
 
    lbl.grid(column=0, row=0)
    txt = Tkinter.Entry(top,width=10)
    txt.grid(column=1, row=0)
        

        
        
    def clicked(self):
        f = open (self.txt.get(),'r')
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
     
        self.lbl.configure(text="Button was clicked !!")
    
    def client_exit(self):
        exit()

w=windows()
btn = Tkinter.Button(w.top, text="Click Me",command=w.clicked)



 
btn.grid(column=2, row=0)
# creating a button instance
quitButton = Tkinter.Button(w.top,text="Quit",command=w.client_exit)

        # placing the button on my window
quitButton.grid(column=4, row=0)
# Code to add widgets will go here...
w.top.mainloop()

"--------------------------------------------------------------------"

print(vm.opera)

if respuesta==2:
    print('comparame esta\n')
    f = open (txt,'r')
    mensaje2 = f.read()
    
    # Make this false if you need to run the debugger inside a test.
    "CAPTURE_STDOUT = ('-s' not in sys.argv)"
    # Make this false to see the traceback from a failure inside pyvm2.
    CAPTURE_EXCEPTION = 1
    
    
    code=mensaje2
    f.close()
    code = textwrap.dedent(code)
    code = compile(code, "<%s>" % id(code), "exec", 0, 1)
    dis_code(code)
    vm_stdout2 = six.StringIO()
    vm2 = VirtualMachine()
    vm_value2 = vm_exc2 = None
    vm_value2 = vm2.run_code(code)
