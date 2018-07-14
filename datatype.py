#coding=utf-8
class TypeMeta(type): 
    __name__ = "ExprMeta"
    __subs__ = {}
    def __new__(cls,name,parents,attrs):
        #print("new metaclass info: ", cls, name, parents, attrs)  
        attrs["__name__"] = name
        #print( attrs.keys() )
        if '__init__' not in attrs.keys() and parents != ( ): 
            attrs["__init__"] = lambda self: None
        if "__repr__" not in attrs.keys():
            attrs["__repr__"] = lambda self: self.__name__
        if parents == ( ):
            if name not in cls.__subs__.keys():
                cls.__subs__[name] = [ ] # init 
        else:
            for p in parents:
                cls.__subs__[p.__name__] += [name]
        return type.__new__(cls, name, parents, attrs)
    def __instancecheck__(cls,instance):
        if hasattr(instance,"__name__") and hasattr(cls,"__subs__"):
            name = instance.__name__
            if cls.__name__ in cls.__subs__.keys():
                return name in cls.__subs__[cls.__name__]
        return False
    def __repr__(self):
        return self.__name__
class species(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(typ,*args,**kw)
        return wrapper
class static(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(*args,**kw)
        return wrapper
class prop(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(obj,*args,**kw)
        return wrapper()
class class_prop(object):
    def __init__(self,func):
        self.func = func
    def __get__(self,obj,typ=None):
        def wrapper(*args,**kw):
            return self.func(typ,*args,**kw)
        return wrapper()

__all__ = ["TypeMeta","species","static","prop","class_prop"]
