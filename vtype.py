#coding=utf-8
#from typecheck import *
class ListMeta(type): 
    instances = [list,str,range]
    __name__ = "ListMeta"
    def __instancecheck__(cls,instance):
        if type(instance) in cls.instances:
            #print( "Meta" ,instance,object)
            for x in instance:
                if isinstance(x,object):
                    continue
            return True
        return False
class List(metaclass=ListMeta):
    instances = [list,str,range]
    __name__ = "List"
    def __init__(self,typ=object):
        self.typ = typ
    def __repr__(self):
        return '( {} list )'.format(repr(self.typ))
    def __instancecheck__(self,instance):
        if type(instance) in self.instances:
            #print( "List" ,instance,self.typ)
            for x in instance:
                if isinstance(x,self.typ):
                    continue
            return True
        return False
class TupleMeta(type):
    __name__ = "TupleMeta"
class Tuple(metaclass=TupleMeta):
    instances = [tuple]
    __name__ = "Tuple"
    def __init__(self,*typs):
        self.typs = typs
    def __repr__(self):
        return " * ".join( [ i.__name__ for i in self.typs] )
    def __instancecheck__(self,instance):
        if type(instance) in self.instances:
            #print( "Tuple",instance,self.typs )
            for i,t in zip(instance,self.typs):
                if isinstance(i,t):
                    continue
                else:
                    return False
            return True
        return False
class RecordMeta(type): 
    __name__ = "RecordMeta"
class Record(metaclass=RecordMeta):
    instances = [dict]
    def __init__(self,**kw):
        self.kw = kw
    def __instancecheck__(self,instance):
        if type(instance) in self.instances:
            #print( instance.keys() , self.kw.keys() )
            if instance.keys() == self.kw.keys():
                for v,t in zip(instance.values(),self.kw.values()):
                    if isinstance(v,t):
                        continue
                    else:
                        return False
                return True
        return False
class ArrowMeta(type):
    __name__ = "Arrow"
class Arrow(metaclass=ArrowMeta):
    __name__ = "Arrow"
    def __init__(self,source,target):
        self.src_type = source
        self.tag_type = target
        self.info = {
            'Tuple':  self.Tuple,
            'List':   self.List,
            'Record': self.Record,
        }        
    def Tuple(self,s,t):
        return s.typs == t.typs
    def List(self,s,t):
        return s.typ is t.typ
    def Record(self,s,t):
        return s.kw == t.kw
    def __repr__(self):
        return "( {} -> {} )".format(repr(self.src_type),repr(self.tag_type))
    def __instancecheck__(self,instance):
        noAtom = ["Tuple","List","Record"]
        if hasattr(instance,'__annotations__'):
            temp = {}
            temp.update(instance.__annotations__)
            annotations = temp
            if annotations == {}:
                return False
            #print( annotations,instance,instance.__annotations__ )
            ret_typ = annotations["return"]
            annotations.pop('return')
            vs = list(annotations.values())
            tvs = Tuple(*vs)
            if ret_typ.__name__ in noAtom and self.tag_type.__name__ in noAtom:
                ret_flag = self.info[ret_typ.__name__](ret_typ,self.tag_type)
            else:
                ret_flag = ret_typ is self.tag_type
            if self.src_type.__name__ != "Tuple":
                if len(vs) == 1:
                    args_flag = vs[0] is self.src_type
                else:
                    args_flag = False
            else:
                args_flag = self.info["Tuple"](tvs,self.src_type)
            #print( 'ret_flag and args_flag :',(ret_flag,args_flag),instance.__name__,instance.__annotations__)
            #print( "ret_flag:",ret_flag ,ret_typ,self.tag_type)
            return ret_flag and args_flag
        return False
"""
print( 'list',isinstance([1,2,3],List ) )
print( 'range',isinstance(range(1,2,3),List) )
print( 'str',isinstance("123",List(str)) )
print( 'tuple',isinstance( (1,2,3,None),List(int) ) )
print( 'tuple',isinstance( (1,2,3) ,Tuple(int,int,int) ) )
print( '--------------------' )
print( 'record',isinstance( {'a':1,'b':2} ,Record(a=int,b=int) ) )
@check
def tail( lst : List(int) ) -> List(int):
    return lst[1:]
"""
__all__ = ["List","Tuple","Record","Arrow"]
