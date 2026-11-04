from fractions import Fraction as F
from itertools import product
# q29: explicit labeled balls
def run():
    # states: (A list, B list) as tuples of colors with labels
    start=(('W1','K1','K2'),('W2','W3','K3','K4'))
    paths=[(start,F(1),False)]
    for _ in range(3):
        new=[]
        for (A,B),p,diff in paths:
            for i in range(3):
                for j in range(4):
                    a,b=A[i],B[j]
                    nA=tuple(sorted(A[:i]+A[i+1:]+(b,))); nB=tuple(sorted(B[:j]+B[j+1:]+(a,)))
                    new.append(((nA,nB),p/12,diff or a[0]!=b[0]))
        paths=new
    num=sum(p for (A,B),p,d in paths if sum(x[0]=='W' for x in A)==1 and d)
    den=sum(p for (A,B),p,d in paths if sum(x[0]=='W' for x in A)==1)
    r=num/den; print("q29",r,r.numerator+r.denominator)
run()
