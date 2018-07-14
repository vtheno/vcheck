#coding=utf-8
from opcode import cmp_op
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
            return self.push(left_val)
        else:
            error( "for {} type(s): {} and {}".format(cmp_op[args],repr(left_val),repr(right_val) ) )
    def tup(self,args):
        val = tuple( reversed( [self.pop () for i in range(args)] ) )
        return self.push (val)
    def lst(self,args):
        val = list( reversed( [self.pop () for i in range(args)] ) )
        return self.push (val)
    def If(self):
        else_val = self.pop ()
        then_val = self.pop ()
        test = self.pop ()
        print( 'if:',test,then_val,else_val)
        if then_val == else_val:
            return self.push(then_val)
        else:
            error( "for if type(s): {} and {}".format(repr(then_val),repr(else_val)) )
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
