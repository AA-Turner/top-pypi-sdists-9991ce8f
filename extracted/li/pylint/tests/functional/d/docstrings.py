# pylint: disable=unnecessary-pass, consider-using-f-string
# -1: [missing-module-docstring]

# +1: [empty-docstring]
def function0():
    """"""

# +1: [missing-function-docstring]
def function1(value):
    # missing docstring
    print(value)

def function2(value):
    """docstring"""
    print(value)

def function3(value):
    """docstring"""
    print(value)

# +1: [missing-class-docstring]
class AAAA:
    # missing docstring

##     class BBBB:
##         # missing docstring
##         pass

##     class CCCC:
##         """yeah !"""
##         def method1(self):
##             pass

##         def method2(self):
##             """ yeah !"""
##             pass

    # +1: [missing-function-docstring]
    def method1(self):
        pass

    def method2(self):
        """ yeah !"""
        pass

    # +1: [empty-docstring]
    def method3(self):
        """"""
        pass

    def __init__(self):
        pass

class DDDD(AAAA):
    """yeah !"""

    def __init__(self):
        AAAA.__init__(self)

    # +1: [empty-docstring]
    def method2(self):
        """"""
        pass

    def method3(self):
        pass

    # +1: [missing-function-docstring]
    def method4(self):
        pass

# pylint: disable=missing-docstring
def function4():
    pass

# pylint: disable=empty-docstring
def function5():
    """"""
    pass

def function6():
    """ I am a {} docstring.""".format("good")

def function7():
    """docstring"""
    def inner():
        # Not documented
        return 42
    return inner()
