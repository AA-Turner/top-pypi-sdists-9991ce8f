# pylint: disable=undefined-variable, use-list-literal, unnecessary-lambda-assignment, use-dict-literal
"""test suspicious lambda expressions
"""


# Some simple examples of the most commonly encountered forms.
# +1: [unnecessary-lambda]
_ = lambda: list()  # replaceable with "list"
# +1: [unnecessary-lambda]
_ = lambda x: hash(x)  # replaceable with "hash"
# +1: [unnecessary-lambda]
_ = lambda x, y: min(x, y)  # replaceable with "min"

# A function that can take any arguments given to it.
_ANYARGS = lambda *args, **kwargs: 'completely arbitrary return value'

# Some more complex forms of unnecessary lambda expressions.
# +1: [unnecessary-lambda]
_ = lambda *args: _ANYARGS(*args)
# +1: [unnecessary-lambda]
_ = lambda **kwargs: _ANYARGS(**kwargs)
# +1: [unnecessary-lambda]
_ = lambda *args, **kwargs: _ANYARGS(*args, **kwargs)
# +1: [unnecessary-lambda]
_ = lambda x, y, z, *args, **kwargs: _ANYARGS(x, y, z, *args, **kwargs)

# These don't use their parameters in their body
# +1: [unnecessary-lambda]
_ = lambda x: z(lambda x: x)(x)
# +1: [unnecessary-lambda]
_ = lambda x, y: z(lambda x, y: x + y)(x, y)

# Lambdas that are *not* unnecessary and should *not* trigger warnings.
_ = lambda x: x
_ = lambda x: x()
_ = lambda x=4: hash(x)
_ = lambda x, y: list(range(y, x))
_ = lambda x: list(range(5, x))
_ = lambda x, y: list(range(x, 5))
_ = lambda x, y, z: x.y(z)
_ = lambda: 5
_ = lambda **kwargs: _ANYARGS()
_ = lambda **kwargs: _ANYARGS(**dict([('three', 3)]))
_ = lambda **kwargs: _ANYARGS(**{'three': 3})
_ = lambda dict_arg, **kwargs: _ANYARGS(kwargs, **dict_arg)
_ = lambda *args: _ANYARGS()
_ = lambda *args: _ANYARGS(*list([3, 4]))
_ = lambda *args: _ANYARGS(*[3, 4])
_ = lambda list_arg, *args: _ANYARGS(args, *list_arg)
_ = lambda: _ANYARGS(*[3])
_ = lambda: _ANYARGS(**{'three': 3})
_ = lambda: _ANYARGS(*[3], **{'three': 3})
_ = lambda: _ANYARGS(func=42)

# pylint: disable=missing-function-docstring
def f(d):
    print(lambda x: str(x, **d))

# Don't warn about this.
_ = lambda: code().analysis()

_ = lambda **kwargs: dict(bar=42, **kwargs)

# These use the lambda parameters in their body
_ = lambda x: x(x)
_ = lambda x, y: x(x, y)
_ = lambda x: z(lambda y: x + y)(x)
