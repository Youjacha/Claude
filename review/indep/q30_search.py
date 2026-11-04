import mpmath as mp, itertools
mp.mp.dps=30
def f(x,a,b): return mp.power(3,(x-a+8)/4)-b
def g(x,a,b): return 4*mp.log(abs(x+b),3)+a-8
def roots(a,b):
    h=lambda x: f(x,a,b)-g(x,a,b)
    rs=[]
    # scan on both sides of -b
    for lo,hi in [(-b-200,-b-1e-12),(-b+1e-12,-b+200)]:
        xs=[lo+(hi-lo)*k/40000 for k in range(40001)]
        # use log-spacing near -b too
        xs+= [ -b+s*mp.mpf(10)**(-e) for e in range(1,12) for s in (-1,1) if lo< -b+s*mp.mpf(10)**(-e) <hi]
        xs=sorted(xs)
        vals=[h(x) for x in xs]
        for i in range(len(xs)-1):
            if vals[i]==0: rs.append(xs[i])
            elif vals[i]*vals[i+1]<0:
                rs.append(mp.findroot(h,(xs[i],xs[i+1]),solver='bisect'))
            elif abs(vals[i])<1e-6:
                rs.append(xs[i])
    return rs
sols=set()
for a0,b0 in itertools.product(range(-12,13,2),repeat=2):
    try:
        s=mp.findroot(lambda a,b:[f(a,a,b)-g(a,a,b), f(b,a,b)-g(b,a,b)],(a0+0.3,b0-0.7))
    except Exception: continue
    a,b=s
    if abs(a-b)<1e-8: continue
    sols.add((round(float(a),8),round(float(b),8)))
print(sols)
