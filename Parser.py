#coding=utf-8
from TVar import *
from data import *
from opcode import opname,opmap
class ParseError(Exception): pass
def unpack(lst : List(Int) ) -> Tuple(Int,List(Int)) :
    if lst != [ ]:
        return lst[0],lst[1:]
    else:
        raise ParseError("unpack (nil) | {}" .format(lst))
def parseArgs( toks : List(Int) ) -> Tuple( Int,List(Int) ):
    if toks != [ ]:
        return toks[0],toks[1:]
    else:
        raise ParseError("parseArgs (nil) | {}" .format(lst))
def parseAtom( toks : List(Int) ) -> Tuple(Any,List(Int)) :
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
    elif t == opmap["BINARY_POWER"]:
        args,rest1 = parseArgs(rest)
        return ( BIN_OP('**',args),rest1 )
    elif t == opmap["BINARY_TRUE_DIVIDE"]:
        args,rest1 = parseArgs(rest)
        return ( BIN_OP('/',args),rest1 )
    elif t == opmap["BINARY_FLOOR_DIVIDE"]:
        args,rest1 = parseArgs(rest)
        return ( BIN_OP('//',args),rest1 )
    elif t == opmap["BUILD_SLICE"]:
        args,rest1 = parseArgs(rest)
        return ( SLICE(args),rest1 )
    elif t == opmap["BINARY_SUBSCR"]:
        args,rest1 = parseArgs(rest)
        return ( SUB_SCR(args),rest1)
    elif t == opmap["COMPARE_OP"]:
        args,rest1 = parseArgs(rest)
        return ( CMP_OP(args),rest1 )
    elif t == opmap["POP_JUMP_IF_FALSE"]:
        args,rest1 = parseArgs(rest) 
        left = parseDec( rest1[:args] , [ ] )
        right = parseDec( rest1[args:] , [ ]  )
        return ( IF(args,left,right),[] )
    elif t == opmap["CALL_FUNCTION"]:
        args,rest1 = parseArgs(rest)
        return ( CALL(args),rest1 )
    elif t == opmap["FOR_ITER"]:
        args,rest1 = parseArgs(rest)
        block = parseDec( rest1[:args],[ ] )
        rs = rest1[args:]
        return ( FOR(args,block),rs )
    elif t in [0,opmap["NOP"]]:
        args,rest1 = parseArgs(rest)
        return ( NOP(args) ,rest1)
    elif t in opmap.values():
        args,rest1 = parseArgs(rest)
        return ( NOP(args),rest1 )
    else:
        raise ParseError ("ParseAtomError: no match {} , {}".format(repr(t),rest))
def parseExpr( toks : List(Int) ) -> Tuple(Any,List(Int)) :
    exp1,rest1 = parseAtom( toks )
    return parseRest(exp1,rest1)
def parseRest( exp1 : Any,toks : List(Int) ) -> Tuple(Any,List(Int)) :
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

def parse(inp : List(Int) ) -> Any:
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
