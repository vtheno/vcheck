#coding=utf-8
from datatype import TypeMeta
from machine import Stack
class Expr(metaclass=TypeMeta): pass
class Const(Expr): 
    def __init__(self,args):
        self.args = args
class L_FAST(Expr):
    def __init__(self,args):
        self.args = args 
class S_FAST(Expr):
    def __init__(self,args):
        self.args = args 
class L_GLOBAL(Expr):
    def __init__(self,args):
        self.args = args 
class S_GLOBAL(Expr):
    def __init__(self,args):
        self.args = args 
class Tup(Expr):
    def __init__(self,args):
        self.args = args
class Lst(Expr):
    def __init__(self,args):
        self.args = args
class Ret(Expr):
    def __init__(self,args):
        self.args = args 
class BIN_OP(Expr):
    def __init__(self,name,args):
        self.name = name
        self.args = args 
class SLICE(Expr):
    def __init__(self,args):
        self.args = args
class SUB_SCR(Expr):
    def __init__(self,args):
        self.args = args
class CMP_OP(Expr):
    def __init__(self,args):
        self.args = args
class IF(Expr):
    def __init__(self,args,then_dec,else_dec):
        self.args = args
        self.then_dec = then_dec
        self.else_dec = else_dec
    def __repr__(self):
        return "IF [" + repr(self.then_dec) + "," + repr(self.else_dec) + "]"
class FORWARD(Expr):
    def __init__(self,args):
        self.args = args
class CALL(Expr):
    def __init__(self,args):
        self.args = args
class NOP(Expr):
    def __init__(self,args):
        self.args = args
class DEC(Expr):
    def __init__(self,args):
        self.args = args
    def __repr__(self):
        return "DEC " + repr(self.args)
def runout( expr : Expr , s : Stack ):
    if isinstance(expr,DEC):
        for ei in expr.args:
            runout(ei,s)
    elif isinstance(expr,NOP):
        pass
    elif isinstance(expr,Const):
        s.push_const(expr.args)
    elif isinstance(expr,L_FAST):
        s.push_fast(expr.args)
    elif isinstance(expr,S_FAST):
        s.store_fast(expr.args)
    elif isinstance(expr,L_GLOBAL):
        s.push_global(expr.args)
    elif isinstance(expr,S_GLOBAL):
        s.store_global(expr.args)
    elif isinstance(expr,BIN_OP):
        s.binop(expr.name)
    elif isinstance(expr,CMP_OP):
        s.cmpop(expr.args)
    elif isinstance(expr,Tup):
        s.tup(expr.args)
    elif isinstance(expr,Lst):
        s.lst(expr.args)
    elif isinstance(expr,SLICE):
        s.slice(expr.args)
    elif isinstance(expr,SUB_SCR):
        s.sub_scr(expr.args)
    elif isinstance(expr,IF):
        runout(expr.then_dec,s)
        runout(expr.else_dec,s)
        s.If ()
    elif isinstance(expr,CALL):
        s.call(expr.args)
    elif isinstance(expr,Ret):
        s.ret ()
    else:
        raise Exception("Not find {}".format(repr(expr)))
    #print( expr,s.s[:10] )
