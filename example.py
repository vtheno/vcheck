from TVar import *
from check import T
c = "test"
d = 233
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
@T
def main() -> Unit:
    # Unit -> Unit
    func( 123 )
if __name__ == '__main__':
    main ()
#print ( func( 0 ) )
