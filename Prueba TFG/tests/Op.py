"""Testing tools for byterun."""

from __future__ import print_function

import dis
import sys
import textwrap
import types
import unittest

import six

from byterun.pyvm2 import VirtualMachine, VirtualMachineError

f = open ('holamundo.py','r')
mensaje = f.read()
print(mensaje)


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
CAPTURE_EXCEPTION = 1


code=mensaje
f.close()
code = textwrap.dedent(code)
code = compile(code, "<%s>" % id(code), "exec", 0, 1)
dis_code(code)
vm_stdout = six.StringIO()
vm = VirtualMachine()
vm_value = vm_exc = None
vm_value = vm.run_code(code)

