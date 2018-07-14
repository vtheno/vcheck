#coding=utf-8
from opcode import cmp_op
from TVar import *
class CheckError(Exception): pass
def error(msg):
    raise CheckError(msg)
class Stack(object):
    def __init__(self,ltenv,gtenv,ctenv,size=256):
        self.s = [ None ] * size
        self.top = 0
        self.local_tenv = ltenv
        self.global_tenv = gtenv
        self.const_tenv = ctenv
    def push(self,val):
        self.s[self.top] = val
        self.top += 1
        return self.top 
    def pop(self): # RETURN_VALUE = POP
        self.top -= 1
        val = self.s[self.top]
        self.s[self.top] = None
        return val
    def push_const(self,args):
        val = self.const_tenv[args]
        return self.push(val)
    def push_fast(self,args): # LOAD_XXX = PUSH typ-val
        val = self.local_tenv[args]
        #print( 'load-fast:',val,self.s[0:10])
        return self.push(val)
    def store_fast(self,args):
        val = self.pop ( )
        self.local_tenv[args] = val
        return 
    def push_global(self,args):
        val = self.global_tenv[args]
        return self.push(val)
    def store_global(self,args):
        val = self.pop ( )
        self.global_tenv[args] = val
        return 
    def binop(self,name):
        right_val = self.pop ()
        left_val = self.pop ()
        #print( 'binop:',left_val,right_val,self.s[0:10])
        if left_val == right_val:
            return self.push(left_val)
        else:
            error( "for {} type(s): {} and {}".format(name,repr(left_val),repr(right_val) ) )
    def cmpop(self,args):
        right_val = self.pop ()
        left_val = self.pop ()
        #print( 'binop:',left_val,right_val,self.s[0:10])
        if left_val == right_val:
            return self.push(bool)#self.push(left_val)
        else:
            error( "for {} type(s): {} and {}".format(cmp_op[args],repr(left_val),repr(right_val) ) )
    def tup(self,args):
        lst = list(reversed( [self.pop () for i in range(args)] ))
        if lst == [ ]:
            return self.push( Unit )
        val = Tuple( *lst)
        return self.push (val)
    def lst(self,args):
        val = list( reversed( [self.pop () for i in range(args)] )  )
        if val == [ ]:
            return self.push( List(Any) )
        flag = val.pop()
        for v in val:
            if v != flag:
                error( "for {} type(s): {} and {}".format("["+flag+"]",v,flag))
        return self.push ( List(flag) )
    def slice(self,args):
        end = self.pop ()
        start = self.pop ()
        if (end == Unit or end == Int) and ( start == Int or start == Unit ):
            return self.push( [Int] ) 
        else:
            error("for slice type(s): slice({},{})".format(start,end) )
    def sub_scr(self,args):
        index = self.pop ()
        lst = self.pop ()
        if isinstance(lst,List):
            if index == Int :
                typ = lst.tvar[0]
                return self.push(typ)
            elif index == [Int]:
                typ = List(Int)
                return self.push(typ)
            else:
                error("for subscr type(s): {} and {}".format(Int,index) )
        else:
            error("for subscr type(s): {} and {}".format(lst,List) )
    def If(self):
        else_val = self.pop ()
        then_val = self.pop ()
        test = self.pop ()
        #print( 'if:',test,then_val,else_val)
        if then_val == else_val:
            return self.push(then_val)
        else:
            error( "for if type(s): {} and {}".format(repr(then_val),repr(else_val)) )
    def call(self,args):
        arglist = [i for i in reversed( [ self.pop () for z in range(args) ] ) ]
        functyp = self.pop () # TVar TO
        def arp(to,acc):
            if not isinstance(to,To):
                return acc + [to]
            return arp(to.b,acc + [to.a] )
        lst = arp(functyp,[ ])
        ret = lst.pop()
        #print( "arglist:",arglist,"functyp:",functyp , lst )
        if len(arglist) != len(lst):
            error("call function argcount type(s): {} and {}".format(len(arglist),len(lst)) )
        for a,t in zip(arglist,lst):
            #print( a,t ,a == t )
            if a != t:
                error("call function type(s): {} and {}".format(arglist,lst))
        return self.push(ret)
    def ret(self):
        val = self.pop ()
        typ = self.global_tenv["return"]
        if val == typ:
            return self.push(val)
        else:
            error( "for return type(s): {} and {}".format(repr(typ),repr(val) ) )
    @property
    def peek(self):
        return self.s[self.top - 1]


__all__ = ["Stack"]
