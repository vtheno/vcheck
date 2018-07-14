#coding=utf-8
from datatype import TypeMeta
class TVar(metaclass=TypeMeta): pass
class Int(TVar):
    def __ge__(self,other):
        return To(self,other)

Int = Int()
class Str(TVar):
    def __ge__(self,other):
        return To(self,other)

Str = Str()
class Any(TVar): 
    def __ge__(self,other):
        return To(self,other)
    def __eq__(self,other):
        return True
Any = Any()
class Tuple(TVar):
    def __init__(self,*args):
        self.TVars = tuple(list(args))
    def __eq__(self,other):
        return self.TVars == other
    def __ge__(self,other):
        return To(self,other)
    def __repr__(self):
        return repr(self.TVars)
class List(TVar):
    def __init__(self,tvar):
        self.tvar = [tvar]
    def __ge__(self,other):
        return To(self,other)
    def __eq__(self,other):
        return self.tvar == other
    def __repr__(self):
        return repr(self.tvar)
class To(TVar):
    def __init__(self,a,b):
        self.a = a 
        self.b = b
    def __ge__(self,other):
        return To(other,self)
    def __eq__(self,other):
        if isinstance(other,To):
            return self.a == other.a and self.b == other.b
        return False
    def __repr__(self):
        return "({} -> {})".format(repr(self.a),repr(self.b))
"""
print( Tuple(Int,Int) == Tuple(Int,Str) )
print( (Int,Int) == (Int,Int) )
print( Tuple(Int,Int) == (Int,Int) )
print( List(Int) == [Int] )
print( (Int >= Int) == (Int >= Int) )
"""
#print( ( Int >= (List(Int) >= Any) ) == (Int >= (List(Int) >= Any)) )
# == Int > List(Int) > Any )
__all__ = ["Int","Str","Any","List","Tuple","TVar","To"]
