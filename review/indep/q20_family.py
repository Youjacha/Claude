import mpmath as mp
# fix alpha=-1, solve beta,gamma,c
def G(x,a,b,g,c): # integral_0^x c(t-a)(t-b)(t-g)
    e1=a+b+g; e2=a*b+b*g+a*g; e3=a*b*g
    return c*(x**4/4 - e1*x**3/3 + e2*x**2/2 - e3*x)
for a in (-1,-0.5,-2):
  try:
    b,g,c=mp.findroot(lambda b,g,c:[G(g,a,b,g,c),G(a,a,b,g,c)+1,G(b,a,b,g,c)-5],(1,3,1))
    f=lambda t:c*(t-a)*(t-b)*(t-g)
    hA=-mp.quad(lambda t:abs(f(t)),[a,0]); hG=mp.quad(lambda t:abs(f(t)),[0,b,g])
    gz=[x for x in mp.linspace(-10,10,4001)]
    print(a,float(b),float(g),float(c),'h sum',float(hA+hG),'int|f|',float(mp.quad(lambda t:abs(f(t)),[a,0,b,g])))
  except Exception as e: print(a,'fail',e)
