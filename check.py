#coding=utf-8
from Parser import *
import dis
from machine import Stack
from data import runout
from opcode import opmap
def get(name,te1,te2):
    if name in te1.keys():
        return te1[name]
    else:
        return te2[name]

class T(object):
    def __init__(self,func):
        self.func = func
        self.global_env = func.__globals__
        self.t_env_1 = {}
        self.t_env_2 = {}
        self.t_env_1.update( func.__annotations__ )
        self.co = func.__code__
        self.bins = list( self.co.co_code )
        if None in self.co.co_consts and self.bins[-4:] == [opmap["LOAD_CONST"],0,opmap["RETURN_VALUE"],0]:
            self.toks = self.bins[0:-4]
        else:
            self.toks = self.bins
        n = 0
        while n < len(self.toks):
            op,args = self.toks[n],self.toks[n+1]
            if op == opmap["POP_JUMP_IF_FALSE"]:
                self.toks[n + 1] = args - n - 2
            elif op == opmap["JUMP_FORWARD"]:
                self.toks[n] = 0
                self.toks[n + 1] = 0
            n+=2
        self.e_names = dict( zip(range(len(self.co.co_names)),
                                 [type(self.global_env.get(i,None)) for i in self.co.co_names]) )
        # e_names = global_env
        self.e_consts = dict( zip(range(len(self.co.co_consts)),
                                  [type(i) for i in self.co.co_consts]) )
        self.e_varnames = dict( zip(range(len(self.co.co_varnames)), 
                                    [self.t_env_1.get(i,type(None)) for i in self.co.co_varnames] ))
        self.e_names.update( {'return':self.t_env_1['return']} )
        self.st = Stack( self.e_varnames,self.e_names,self.e_consts)
        # ltenv gtenv ctenv , stack size
        dis.dis(func)
        print( self.e_varnames,self.e_names,self.e_consts)
        self.parse()
        
    def parse(self):
        out = parse(self.toks)
        print( "runout:",out )
        print( runout(out,self.st) )
    def __call__(self):
        pass

        
c = object()
d = 233
@T
def add( a : int ,b: int ) -> (int,object):
    if a >= b :
        if a == b:
            return (d,c)
        else:
            return (a,c)
    else:
        return (b,c)

#dis.dis(add)
