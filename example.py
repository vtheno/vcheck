from TVar import *
from check import T
c = "test"
d = 233
"""
@T
def add( a : Int ,b: Int ) -> Tuple(Int,Any):
    if a >= b :
        if a == b:
            return (d,c)
        else:
            return (a,c)
    else:
        return (b,c)
@T
def func( a : Int ) -> Unit:#(Int,Any):
    print( add(a,a) )
    return 
"""
@T
def sum( lst : List(Int) ) -> Int:
    if lst == [ ]:
        return 0
    else:
        return lst[0] + sum(lst[1:])
"""
@T
def main() -> Unit:
    # Unit -> Unit
    func( 123 )

if __name__ == '__main__':
    main ()
"""
#print ( func( 0 ) )
#print ( sum( [1,2,3,4] ) )
