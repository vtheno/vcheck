#coding=utf-8
from Parser import *
import dis
from machine import Stack
from data import runout
from opcode import opmap
from TVar import *
from types import FunctionType
class getTypeError(Exception): pass
def getType(obj):
    vals = [int,str,type(None)]
    keys = [Int,Str,Unit]
    env = dict(zip(vals,keys))
    if isinstance(obj,TVar):
        return obj
    elif type(obj) in vals:
        return env[type(obj)]
    elif type(obj) == FunctionType:
        def arp(lst,acc):
            if lst == [ ]:
                return acc
            return arp(lst[1:], To( lst[0] ,acc ) )
        f = [i for i in obj.__annotations__.values() ] 
        l = f.pop()
        #print( "arp:",arp(f,l ) )
        return arp(f,l)
    elif isinstance(obj,T):
        return getType(obj.func)
    elif isinstance(obj,tuple):
        return Tuple( *[getType(i) for i in obj] )
    elif ( isinstance(obj,list) and len(obj) == 1):
        for i in obj:
            if not isinstance(i,TVar):
                raise getTypeError("Get Type Error for: {}".format(( type(obj),obj)) )
        return obj
    else:
        raise getTypeError("Get Type Error for: {}".format(( type(obj),obj)) )
class T(object):
    def clear(self):
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
    def __init__(self,func):
        self.func = func
        self.t_env_1 = {}
        self.t_env_1.update ( func.__annotations__ )
        self.t_env_2 = {}
        self.t_env_2.update ( func.__globals__ )
        self.t_env_2.update ( {'str':To(Any,Str),'int':To(Any,Int),'print':To(Any,Unit) } )
        self.t_env_2.update ( { func.__name__ : func } )
        self.co = func.__code__
        self.bins = list( self.co.co_code )
        self.clear()
        def processName(lst):
            nlst = [ ]
            for i in lst:
                t = self.t_env_2.get(i,None)
                t = getType(t)
                nlst += [t]
            return nlst
        def processConst(consts):
            nconsts = [ ]
            for i in consts:
                t = getType(i)
                nconsts += [ t ]
            return nconsts
        def processLocal(local):
            alocal = [ ]
            for i in local:
                t = self.t_env_1.get(i,None)
                t = getType(t)
                alocal += [ t ]
            return alocal
        # process function name to functype
        self.e_names = dict( zip(range(len(self.co.co_names)),processName(self.co.co_names) ) )
        self.e_consts = dict( zip(range(len(self.co.co_consts)),processConst(self.co.co_consts)) )
        self.e_varnames = dict( zip(range(len(self.co.co_varnames)), processLocal(self.co.co_varnames) ) )
        self.e_names.update( {'return':self.t_env_1['return']} )
        self.st = Stack( self.e_varnames,self.e_names,self.e_consts)
        # ltenv gtenv ctenv , stack size
        dis.dis(func)
        print( self.e_varnames,self.e_names,self.e_consts)
        self.parse()
        print( self.st.global_tenv,self.st.local_tenv,self.st.const_tenv )
        
    def parse(self):
        out = parse(self.toks)
        #print( "runout:",out )
        runout(out,self.st)
    def __call__(self,*args,**kds):
        return self.func(*args,**kds)


__all__ = ["T"]
