"""2027-09 변별 문항 검증 스크립트 (analysis/discrimination/2027-09.md 부록).
실행: python3 -I analysis/discrimination/scripts/2027-09_verify.py  (sympy, numpy 필요, 수 분 소요)"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import math, sympy as sp
x,t=sp.symbols('x t',real=True)
def icbrt(k):
    m=round(k**(1/3))
    for c in (m-1,m,m+1):
        if c>0 and c**3==k: return c
def iroot(k,e):
    m=round(k**(1/e))
    for c in (m-1,m,m+1):
        if c>0 and c**e==k: return c
print("=== Q14")
def q14(N,term_cube):
    s=F(0);c=0
    for n in range(1,N+1):
        m=icbrt(n); s+= term_cube(n,m) if m else F(n)
        c+= s.denominator==1
    return c
print("answer",q14(300,lambda n,m:F(m*m,5)))
print("M-structure", [(M, sum(i*i for i in range(1,M+1))%5) for M in range(1,7)])
print("wrong: skip k=1 cube",q14(300,lambda n,m:F(n) if m==1 else F(m*m,5)))
print("wrong: cube term m/5",q14(300,lambda n,m:F(m,5)))
print("wrong: cube term 1/(5m)... ",q14(300,lambda n,m:F(1,5*m)))
print("wrong: cube term m^3/5",q14(300,lambda n,m:F(m**3,5)))
print("wrong: count n<300",q14(299,lambda n,m:F(m*m,5)))
print("T14 template (sqrt, c=3, n<=100):")
def t14(N,c):
    s=F(0);cnt=0
    for n in range(1,N+1):
        m=iroot(n,2); s+= F(m,c) if m else F(n)   # f(sqrt k)/(c f(k)): (1/m)/(c/m^2)=m/c
        cnt+= s.denominator==1
    return cnt
print("  count",t14(100,3), " M with M(M+1)/2%3==0:",[M for M in range(1,11) if M*(M+1)//2%3==0])

print("=== Q15")
f=(x+2)*(x+sp.Rational(1,2)); print("f expand",sp.expand(f),"f(2)=",f.subs(x,2))
def lim_ok(f,num,tv):
    D=sp.expand(f+f.subs(x,x-tv)); rs=sp.Poly(D,x).all_roots() if sp.Poly(D,x).degree()>0 else []
    for r in set(rs):
        if not r.is_real: continue
        L=sp.limit(num*f/D,x,r,'+'); R=sp.limit(num*f/D,x,r,'-')
        if not (L.is_finite and R.is_finite and L==R): return False
    return True
res=[(tv,lim_ok(f,2*x+1,tv)) for tv in [sp.Rational(k,8) for k in range(1,21)]]
print("t ok:",[str(a) for a,b in res if b]); print("t fail:",[str(a) for a,b in res if not b])
fw=(x+sp.Rational(1,2))*(x-1); print("wrong orientation f=(x+1/2)(x-1) f(2)=",fw.subs(x,2))
fv=(x+sp.Rational(1,2))**2-sp.Rational(9,16); print("wrong vertex at -1/2 f(2)=",fv.subs(x,2))
print("T15 template: num (x-2), set t>=2, f=x(x-2)")
g=x*(x-2); res=[(tv,lim_ok(g,x-2,tv)) for tv in [sp.Rational(k,4) for k in range(1,13)]]
print("  t ok:",[str(a) for a,b in res if b]," f(5)=",g.subs(x,5))

print("=== Q20")
a=sp.symbols('a',positive=True)
A=(a,sp.sin(a)); B=(sp.pi+a,-sp.sin(a)); C=(2*sp.pi-a,sp.sin(a)); D=(sp.pi-a,-sp.sin(a))
k=-sp.tan(a)
for P,name,fx in [(A,'A',True),(B,'B',True),(C,'C',False),(D,'D',False)]:
    av=sp.Rational(7,10)*sp.pi
    gv=sp.simplify((-k*sp.cos(P[0])-P[1]).subs(a,av)); fv_=sp.simplify((sp.sin(P[0])-P[1]).subs(a,av))
    print(name,"on g:",sp.nsimplify(gv)==0, "on f:" ,sp.N(fv_) if fx else '-')
area=lambda P,Q,R: sp.Abs((Q[0]-P[0])*(R[1]-P[1])-(R[0]-P[0])*(Q[1]-P[1]))/2
O=(0,0); shoe=lambda P,Q,R: ((Q[0]-P[0])*(R[1]-P[1])-(R[0]-P[0])*(Q[1]-P[1]))/2
aod=sp.simplify(-shoe(O,A,D)); cdb=sp.simplify(shoe(C,D,B)); print("AOD signed area:",aod," CDB:",cdb)
s=sp.solve(sp.Eq(aod/cdb,sp.Rational(5,14)),a); print(" alpha:",s)
al=sp.Rational(7,10)*sp.pi; print("answer",sp.simplify(3*(sp.pi+al)/(sp.pi-al)), " k=",sp.N(-sp.tan(al)))
print("wrong: AOD as (pi-a)sin a -> a=",sp.solve(sp.Eq((sp.pi-a)/(2*a),sp.Rational(5,14)),a), "3p/q=",sp.simplify(3*(sp.pi+7*sp.pi/12)/(sp.pi-7*sp.pi/12)))
al2=2*sp.pi/3; print("T20 template a=2pi/3: AOD:CDB=",sp.simplify(sp.pi/(4*al2))," k=",sp.simplify(-sp.tan(al2))," 3p/q=",sp.simplify(3*(sp.pi+al2)/(sp.pi-al2)))

print("=== Q21")
def hfun(p,q,av,lam=7,b=4):
    def h(z):
        fz=(z-p)**2*(z-q); g=-fz if fz>=0 else lam*fz
        return g+abs((z-1)*(z-av)*(z-b+av))
    return h
def diffable(h,pts,eps=1e-6):
    for z in pts:
        L=(h(z)-h(z-eps))/eps; R=(h(z+eps)-h(z))/eps
        if abs(L-R)>1e-3: return False
    return True
def search(lam=7,b=4,ask=0.0):
    sols=set()
    grid=[i/4 for i in range(-24,33)]
    for p in grid:
        for q in grid:
            if p==q: continue
            for av in grid:
                h=hfun(p,q,av,lam,b)
                if diffable(h,{p,q,1,av,b-av}): sols.add((p,q,av))
    return sols
S=search(); print("solutions (p,q,a):",sorted(S))
vals=sorted({-p*p*q for p,q,_ in S}); print("f(0) values",vals," answer",max(vals)*min(vals))
print("wrong: only a in{1,3}:",(-12)*(-48)," only a=2:",F(-1,4)*F(-9,4)," only p<q:",(-12)*F(-1,4)," only p>q:",(-48)*F(-9,4))
S2=search(b=6); vals2=sorted({(-1-p)**2*(-1-q) for p,q,_ in S2})
print("T21 template b=6 (roots 1,a,6-a), ask f(-1): sols",sorted(S2)," vals",vals2," max*min",max(vals2)*min(vals2))

print("=== Q22")
import numpy as np
def inters(fun1,fun2,lo,hi,N=200000):
    xs=np.linspace(lo,hi,N); d=fun1(xs)-fun2(xs); r=[]
    for i in range(N-1):
        if d[i]==0 or d[i]*d[i+1]<0:
            a_,b_=xs[i],xs[i+1]
            for _ in range(60):
                m=(a_+b_)/2
                if (fun1(a_)-fun2(a_))*(fun1(m)-fun2(m))<=0: b_=m
                else: a_=m
            r.append((a_+b_)/2)
    return r
av=(81/16)**(1/3)
E=lambda X: av**X; P1=lambda X:2*X**2-3.5*X+3
L=lambda X: np.log(X-0.25)/np.log(av)-0.25; P2=lambda X:2*X**2-7.5*X+7.5
r1=inters(E,P1,-10,10); r2=inters(L,P2,0.2500001,20)
print("E∩P1 x:",[round(v,6) for v in r1]," L∩P2 x:",[round(v,6) for v in r2])
pts=[(v,E(v)) for v in r1]+[(v,L(v)) for v in r2]; print("points",[(round(a_,4),round(b_,4)) for a_,b_ in pts])
Apt,Bpt=pts[0],pts[1]; Dpt,Cpt=pts[-2],pts[-1]
AB=np.subtract(Bpt,Apt); BC=np.subtract(Cpt,Bpt); print("AB",AB,"BC",BC,"dot",np.dot(AB,BC))
print("P2 == P1 shifted (1,-1):",sp.expand(2*(x-1)**2-sp.Rational(7,2)*(x-1)+3-1))
print("a^3 =",F(3,2)**4,"p+q=",81+16)
# uniqueness scan over a: for each a, check if the 4 intersection points can form a rectangle
def rect_resid(av):
    E=lambda X: av**X; L=lambda X: np.log(X-0.25)/np.log(av)-0.25
    r1=inters(E,P1,-10,10,20000); r2=inters(L,P2,0.2500001,30,20000)
    if len(r1)<2 or len(r2)<2: return None
    best=1e9
    import itertools
    for (a1,a2) in itertools.combinations(r1,2):
        for (c1,c2) in itertools.combinations(r2,2):
            Aa=np.array([a1,E(a1)]);Bb=np.array([a2,E(a2)])
            for Cc,Dd in [(np.array([c1,L(c1)]),np.array([c2,L(c2)])),(np.array([c2,L(c2)]),np.array([c1,L(c1)]))]:
                # rectangle ABCD: A+C==B+D and |AC|==|BD|
                best=min(best,np.linalg.norm(Aa+Cc-Bb-Dd)+abs(np.linalg.norm(Aa-Cc)-np.linalg.norm(Bb-Dd)))
    return best
scan=[(round(v,3),rect_resid(v)) for v in np.linspace(1.05,4,60)]
print("scan min-resid a values (resid<0.05):",[(v,round(r,4)) for v,r in scan if r is not None and r<0.05])
print("a_true",round(av,4),"resid",rect_resid(av))
# T22 template: leading coef 4, reflection line y=x-3/4
c=sp.Rational(3,4); d=sp.Rational(3,4)+c
P1t=4*x**2-8*x+sp.Rational(21,4); print("T22 P1t through A,B:",P1t.subs(x,sp.Rational(3,4)),P1t.subs(x,sp.Rational(3,2)))
P2t=sp.expand(P1t.subs(x,x-d)-d); print("T22 P2t=",P2t, " log curve y=log_a(x-3/4)-3/4")
Lt=lambda X: np.log(X-0.75)/np.log(av)-0.75; P2tf=sp.lambdify(x,P2t,'numpy'); P1tf=sp.lambdify(x,P1t,'numpy')
print("  E∩P1t:",[round(v,5) for v in inters(E,P1tf,-10,10)]," Lt∩P2t:",[round(v,5) for v in inters(Lt,P2tf,0.7500001,20)])

print("=== Q28")
def run(start,ks,nswap):
    c=list(start)
    for k in ks:
        if k<=nswap: c[k-1],c[k]=c[k],c[k-1]
    return ''.join(c)
den=num=0; cat=Counter()
for ks in product(range(1,7),repeat=4):
    if run('AAABBB',ks,5)=='AAABBB':
        den+=1; num+= ks[2]==6; cat[ks.count(3)]+=1
print("den",den,"num",num,F(num,den)," by #3s:",dict(cat))
den2=num2=0
for ks in product(range(1,7),repeat=4):
    if run('AAABBB',ks,5)=='AAABBB' and ks[2]==6: num2+=1
print("wrong: only no-3 sequences -> num/den",F(sum(1 for ks in product([1,2,4,5,6],repeat=4) if ks[2]==6),625))
print("T28 template: AABB, die k<=3 swap k,k+1; 3 trials back to AABB; P(2nd trial k>=4)")
den=num=0
for ks in product(range(1,7),repeat=3):
    if run('AABB',ks,3)=='AABB':
        den+=1; num+= ks[1]>=4
print("  ",num,den,F(num,den))

print("=== Q29")
def q29(N,A,cond):
    return sum(1 for a in range(1,N) for b in range(1,N) for c in range(1,N) for d in range(1,N) if a+b+c+d==N and cond(a,b,c,d))
print("answer",q29(14,10,lambda a,b,c,d:10*a>=d and c<d*d), "total",math.comb(13,3))
print("viol 10a<d",q29(14,10,lambda a,b,c,d:10*a<d)," viol c>=d^2 by d:",[q29(14,10,lambda a,b,c,d,D=D:d==D and c>=d*d) for D in range(1,5)])
print("wrong: ignore 10a>=d",q29(14,10,lambda a,b,c,d:c<d*d)," wrong: c<=d^2",q29(14,10,lambda a,b,c,d:10*a>=d and c<=d*d))
print("wrong: nonneg ints",sum(1 for a in range(0,15) for b in range(0,15) for c in range(0,15) for d in range(0,15) if a+b+c+d==14 and 10*a>=d and c<d*d))
print("T29 template N=12, 5a>=d, c<2d:",q29(12,5,lambda a,b,c,d:5*a>=d and c<2*d), " total",math.comb(11,3))

print("=== Q30")
P=Counter()
for tt in product([0,1,2],repeat=5): P[sum(tt)]+=F(1,243)
a30=sum(k*k*P[k] for k in range(1,11)); print("a",a30,"6a",6*a30, " via 25(V/5+1)=",25*(F(2,3)/5+1))
print("wrong E^2 only:",6*25*1," wrong V not /n:",6*25*(F(2,3)+1)," wrong k not k^2:",6*sum(k*P[k] for k in range(1,11)))
P=Counter()
for tt in product([1,2,3],repeat=4): P[sum(tt)]+=F(1,81)
aT=sum(k*k*P[k] for k in range(4,13)); print("T30 balls 1,2,3 n=4: a=",aT," formula 16(V/4+4)=",16*(F(2,3)/4+4)," 3a=",3*aT)
n=10;p=F(2,5)
aB=sum(k*k*math.comb(n,k)*p**k*(1-p)**(n-k) for k in range(0,n+1)); print("T30-모비율: phat n=10 p=2/5: sum k^2 P(phat=k/10)=",aB," =100(p(1-p)/10+p^2)=",100*(p*(1-p)/10+p*p))

# ---- 추가: Q28 분해, Q22 유일성 스캔 ----
two=Counter(); two6=0
for ks in product(range(1,7),repeat=4):
    if run('AAABBB',ks,5)=='AAABBB' and ks.count(3)==2:
        ab=[k for k in ks if k in (2,3,4)]
        two[tuple(ab)]+=1; two6+= ks[2]==6
print("two-3 returning by effective-move pattern:",dict(two)," with 3rd=6:",two6)
print("one-3 or three-3 returning:",sum(1 for ks in product(range(1,7),repeat=4) if run('AAABBB',ks,5)=='AAABBB' and ks.count(3)%2==1))
# Q22 fine scan
P1=lambda X:2*X**2-3.5*X+3; P2=lambda X:2*X**2-7.5*X+7.5
def inters(f1,f2,lo,hi,N=20000):
    xs=np.linspace(lo,hi,N); d=f1(xs)-f2(xs); r=[]
    for i in range(N-1):
        if d[i]*d[i+1]<0:
            a,b=xs[i],xs[i+1]
            for _ in range(50):
                m=(a+b)/2
                if (f1(a)-f2(a))*(f1(m)-f2(m))<=0: b=m
                else: a=m
            r.append((a+b)/2)
    return r
import itertools
def resid(av):
    E=lambda X: av**X; L=lambda X: np.log(X-0.25)/np.log(av)-0.25
    r1=inters(E,P1,-10,12); r2=inters(L,P2,0.2500001,40)
    best=1e9
    for a1,a2 in itertools.combinations(r1,2):
        for c1,c2 in itertools.combinations(r2,2):
            A=np.array([a1,E(a1)]);B=np.array([a2,E(a2)])
            for C,D in [(np.array([c1,L(c1)]),np.array([c2,L(c2)])),(np.array([c2,L(c2)]),np.array([c1,L(c1)]))]:
                best=min(best,np.linalg.norm(A+C-B-D)+abs(np.linalg.norm(A-C)-np.linalg.norm(B-D)))
    return best
grid=np.linspace(1.02,6,500); R=[(resid(v),v) for v in grid]
R=[r for r in R if r[0]<1e8]; R.sort(); print("Q22 smallest residuals (resid,a):",[(round(r,4),round(v,4)) for r,v in R[:5]], " true a=",round((81/16)**(1/3),4))

# Q28 오답 경로: S1에서도 중립을 {1,2,4,5,6}으로 본 잘못된 모형 -> 776, 140, 35/194
den_w=5**4+sum(1 for ks in product(range(1,7),repeat=4) if ks.count(3)==2)+1
num_w=5**3+sum(1 for ks in product(range(1,7),repeat=4) if ks.count(3)==2 and ks[2]==6)
print("Q28 wrong model",den_w,num_w,F(num_w,den_w))
