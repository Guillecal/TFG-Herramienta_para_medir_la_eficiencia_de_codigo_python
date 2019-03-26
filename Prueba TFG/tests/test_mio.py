"""Basic tests for Byterun."""

from __future__ import print_function
from . import vmtest
from . import Op

import six

PY3, PY2 = six.PY3, not six.PY3


class TestIt(vmtest.VmTestCase):
    i=0
    x=1
    y=x+i
    print('Hola')
    print("Hola")
    def test_constant(self):
        self.assert_ok("""\
        x=0 
        y=1
        for z in range(0,5):
            w=y+x
        """)
        print('Hola')
        
Testi=TestIt()
Testi.test_constant()
"""\
        x=0 
        y=1
        w=y+x
        """
"BINARY_ADD"
"BINARY_SUBTRACT"
"BINARY_MULTIPLY"
"BINARY_TRUE_DIVIDE"
