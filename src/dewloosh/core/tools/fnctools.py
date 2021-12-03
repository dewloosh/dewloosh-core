# -*- coding: utf-8 -*-
from functools import reduce


def chain1(*funcs):
    def foo(*args, **kwargs):
        res = funcs[-1](*args, **kwargs)
        for func in funcs[:-1]:
            res = func(res)
        return res
    return foo


def chain2(*funcs):
    def bop(f1, f2):
        def foo(*args, **kwargs):
            return f1(f2(*args, **kwargs))
        return foo
    return reduce(bop, funcs)


def chain3(*funcs):
    def foo(*args, **kwargs):
        if len(funcs) == 1:
            return funcs[0](*args, **kwargs)
        else:
            return funcs[0](chain3(*funcs[1:])(*args, **kwargs))
    return foo


if __name__ == '__main__':

    def lambdagen1d(start, stop): return map(
        lambda p: lambda x: x**p, range(start, stop))

    def f(x): return x**2
    def g(x): return x + 1

    h = chain1(f, g)
    print(h(2))
    print(h(3))

    print("------\n")

    m = chain2(f, g)
    print(m(2))
    print(m(3))

    print("------\n")

    k = chain3(f, g)
    print(k(2))
    print(k(3))

    print("------\n")

    for f in lambdagen1d(0, 4):
        print(f(2))
