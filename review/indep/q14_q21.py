from itertools import permutations
from sympy.utilities.iterables import multiset_permutations
# q14
s=[]
for a1 in range(1,5000):
    a=a1
    for _ in range(5):
        a = 3*a-2 if a<=4 else a-4
    if a==4: s.append(a1)
print("q14",s,sum(s))
# q21
c=0
for p in multiset_permutations(list("AAABBBCCCC")):
    if any(p[k]=='A'==p[k+1] for k in range(9)): continue
    if sum(1 for k in range(9) if {p[k],p[k+1]}=={'A','B'})==4: c+=1
print("q21",c)
