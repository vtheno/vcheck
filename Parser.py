#coding=utf-8
from vtype import *
from data import *
from opcode import opname,opmap
class ParseError(Exception): pass
def strip( tok : int ,toks : List(int) ) -> List(int) :
    #print( "strip:",tok,toks)
    if toks == [ ]:
        raise ParseError("strip error ,rest is nil \n tok: {} rest: {}".format(repr(tok),toks))
    else:
        x,xs = toks[0],toks[1:]
        if tok == x:
            return xs
        else:
            raise ParseError("strip no match tok ,{} , {}".format(repr(tok),toks))
def unpack(lst : List(int) ) -> Tuple(int,List(int)) :
    if lst != [ ]:
        return lst[0],lst[1:]
    else:
        raise ParseError("unpack (nil) | {}" .format(lst))

def parseArgs( toks : List(int) ) -> Tuple( int,List(int) ):
    return toks[0],toks[1:]
def parseAtom( toks : List(int) ) -> Tuple(object,List(int)) :
    t,rest = unpack(toks)
    if t == opmap["LOAD_CONST"]:
        args,rest1 = parseArgs(rest)
        return ( Const(args),rest1 )
    elif t == opmap["LOAD_FAST"]:
        args,rest1 = parseArgs(rest)
        return ( L_FAST(args),rest1 )
    elif t == opmap["STORE_FAST"]:
        args,rest1 = parseArgs(rest)
        return ( S_FAST(args),rest1 )
    elif t == opmap["LOAD_GLOBAL"]:
        args,rest1 = parseArgs(rest)
        return ( L_GLOBAL(args),rest1 )
    elif t == opmap["STORE_GLOBAL"]:
        args,rest1 = parseArgs(rest)
        return ( S_GLOBAL(args),rest1 )
    elif t == opmap["RETURN_VALUE"]:
        args,rest1 = parseArgs(rest)
        return ( Ret(args),rest1 )
    elif t == opmap["BUILD_TUPLE"]:
        args,rest1 = parseArgs(rest)
        return ( Tup(args),rest1 )
    elif t == opmap["BUILD_LIST"]: 
        args,rest1 = parseArgs(rest)
        return ( Lst(args),rest1 )
    elif t == opmap["BINARY_ADD"]:
        args,rest1 = parseArgs(rest)
        return ( BIN_OP('+',args),rest1 )
    elif t == opmap["BINARY_SUBTRACT"]:
        args,rest1 = parseArgs(rest)
        return ( BIN_OP('-',args),rest1 )
    elif t == opmap["BINARY_MULTIPLY"]:
        args,rest1 = parseArgs(rest)
        return ( BIN_OP('*',args),rest1 )
    elif t == opmap["BINARY_TRUE_DIVIDE"]:
        args,rest1 = parseArgs(rest)
        return ( BIN_OP('/',args),rest1 )
    elif t == opmap["COMPARE_OP"]:
        args,rest1 = parseArgs(rest)
        return ( CMP_OP(args),rest1 )
    elif t == opmap["POP_JUMP_IF_FALSE"]:
        args,rest1 = parseArgs(rest) 
        left = parseDec( rest1[:args] , [ ] )
        right = parseDec( rest1[args:] , [ ]  )
        return ( IF(args,left,right),[] )
    elif t == opmap["JUMP_FORWARD"]:
        args,rest1 = parseArgs(rest)
        return ( FORWARD(args),rest1[args:] )
    elif t in [0,opmap["NOP"]]:
        args,rest1 = parseArgs(rest)
        return ( NOP(args) ,rest1)
    else:
        raise ParseError ("ParseAtomError: no match {} , {}".format(repr(t),rest))
def parseExpr( toks : List(int) ) -> Tuple(object,List(int)) :
    exp1,rest1 = parseAtom( toks )
    return parseRest(exp1,rest1)
def parseRest( exp1 : object,toks : List(int) ) -> Tuple(object,List(int)) :
    if toks == [ ]: 
        return (exp1,toks)
    return (exp1,toks)
def parseDec( toks , acc ) :
    if toks == [ ]:
        return DEC( acc )
    e1,rest1 = parseExpr(toks)
    return parseDec(rest1,acc + [e1])
"""
E = T Eopt
Eopt = '+' T Eopt | '-' T Eopt
T = Atom Topt
Topt = '*' Atom Topt | '/' Atom Topt
Atom = Num ... 
DEC = E | DEC
"""

def parse(inp : List(int) ) -> object:
    #return parseExpr( inp )
    return parseDec( inp , [ ] )
def read(inps):
    result,rest = parse(inps)
    if rest == [ ]:
        return result
    else:
        out = implode(rest)
        raise ParseError( "readError:\nno parse all ,error in there: \n {} \n index: {}, {}".format(repr(inps),
                                                                                        len(inps) - len(out),
                                                                                        out) )
__all__ = ["read","parse"]
