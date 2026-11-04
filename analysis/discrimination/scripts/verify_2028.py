"""2028 예시문항 4점 변별 문항 정답 재검증 + 재사용 템플릿 수치 검증.
실행: python3 verify_2028.py  (sympy, mpmath 필요)"""
from sympy import *
from itertools import permutations, product
from fractions import Fraction
from math import comb
import mpmath as mp

x, t, k = symbols('x t k', real=True)
out = {}

# ---------- Q14 ----------
def q14(a4, d, e):
    # a_{n+1} = a_n - d*k (n<=3), k*a_n + e (n>=4), a_4 = a4
    a = {4: a4}
    for n in (3, 2, 1): a[n] = a[n+1] + d*k
    for n in (4, 5, 6): a[n+1] = expand(k*a[n] + e)
    ks = [r for r in solve(Eq(a[1], a[7]), k) if r.is_real]
    vals = {r: abs(a[1].subs(k, r)) + abs(a[2].subs(k, r)) for r in ks}
    return ks, vals, max(vals.values())
out['Q14'] = q14(2, 2, 2)
out['T14'] = q14(1, 1, 1)

# ---------- Q16 ----------
def count_hits(trig, a, b, level=1):
    # [0,2pi] 에서 |2 trig(a x) + b| = level 의 해 개수 (정확 계산)
    T = 2*pi*a  # theta = a x in [0, T]
    sols = set()
    for v in (Rational(level - b, 2), Rational(-level - b, 2)):
        if abs(v) > 1: continue
        base = solveset(trig(t) - v, t, Interval(0, 2*pi))
        for s in base:
            for j in range(0, a + 1):
                th = nsimplify(s + 2*pi*j)
                if 0 <= th <= T: sols.add(th)
    return len(sols)
def q16(trig, N, bmax=6, amax=40):
    pairs = [(a, b) for a in range(1, amax) for b in range(1, bmax) if count_hits(trig, a, b) == N]
    s = [a + b for a, b in pairs]
    return pairs, max(s) + min(s)
out['Q16'] = q16(sin, 10)
out['T16'] = q16(cos, 12)

# ---------- Q18 ----------
def q18(m1, m2, ask):
    p, q, r = symbols('p q r')
    F = m1*x + (x - p)*(x - q)*(x - r)
    G = m1*x + (x - p)*(x - q)
    eqs = []
    for P in ((F - m1*x)*(G - m1*x), (F + m2*x)*(G + m2*x)):
        P = expand(P)
        eqs += [P.coeff(x, i) for i in range(3)]
    sols = [s for s in solve(eqs, [p, q, r], dict=True) if s[p] != s[q]]
    res = set()
    for s in sols:
        f, g = expand(F.subs(s)), expand(G.subs(s))
        res.add((f, g, ask(f, g)))
    return res
out['Q18'] = q18(1, 1, lambda f, g: f.subs(x, 3) + g.subs(x, 8))
out['T18'] = q18(2, 1, lambda f, g: f.subs(x, 4) + g.subs(x, 5))

# ---------- Q19 (좌표 검증) ----------
def q19(b, c):
    A = Matrix([0, 0]); B = Matrix([c, 0])
    C = Matrix([b*cos(2*pi/3), b*sin(2*pi/3)])
    P = C*c/b
    s = symbols('s')
    Qs = [solve(Eq(((B + s*(C - B)).T*(B + s*(C - B)))[0], c**2), s)]
    Q = [B + v*(C - B) for v in Qs[0] if v != 0][0]
    return simplify((P - B).norm()), simplify((C-B).norm()), nsimplify(simplify((P - Q).norm()))
out['Q19'] = q19(5, 3)
out['T19'] = q19(8, 7)

# ---------- Q20 (존재성 + 값) ----------
def q20(hb, hg):
    C, be, de = symbols('C beta delta', positive=True)
    g = C*x*(x - be)**2*(x - de)          # g(0)=g(beta)=g'(beta)=0, beta: 극대
    f = diff(g, x)
    def crit(Cv, bv, dv):
        rs = sorted(float(r) for r in Poly(f.subs({C: Cv, be: bv, de: dv}), x).nroots() if abs(im(r)) < 1e-12)
        return rs
    def F(Cv, bv, dv):
        al, b_, ga = crit(Cv, bv, dv)
        gg = lambda u: float(g.subs({C: Cv, be: bv, de: dv, x: u}))
        return al, b_, ga, gg(al), gg(ga)
    # g(alpha) = -hb/2, g(gamma) = hb - hg 를 만족하는 (C, delta) 를 beta=2 로 고정해 탐색
    bv = 2
    sol = mp.findroot(lambda Cv, dv: (F(Cv, bv, dv)[3] + hb/2, F(Cv, bv, dv)[4] - (hb - hg)), (1, 4))
    Cv, dv = float(sol[0]), float(sol[1])
    al, b_, ga, gal, gga = F(Cv, bv, dv)
    fl = lambda s: float(f.subs({C: Cv, be: bv, de: dv, x: s}))
    hb_num = mp.quad(lambda s: abs(fl(s)), [0, al, b_])
    hg_num = mp.quad(lambda s: abs(fl(s)), [0, al, b_, ga])
    return dict(C=Cv, delta=dv, alpha=al, beta=b_, gamma=ga, g_alpha=gal, g_gamma=gga,
                h_beta=float(hb_num), h_gamma=float(hg_num), answer=gal - gga)
out['Q20'] = q20(8, 24)
out['T20'] = q20(6, 20)

# ---------- Q21 (brute force) ----------
def q21(counts, m):
    cards = [0]*counts[0] + [1]*counts[1] + [2]*counts[2]
    seqs = set(permutations(cards))
    return len(seqs), sum(1 for s in seqs if sum(abs(s[i+1]-s[i]) == 2 for i in range(len(s)-1)) == m)
def q21_struct(counts, m):
    # 1을 지운 0/2 문자열 w 에 1을 끼워 넣는 구조적 계산 (풀이 검증용)
    z, o, w2 = counts
    tot = 0
    for pos in set(permutations([0]*z + [2]*w2)):
        L = len(pos); gaps = L + 1
        alt = [i for i in range(L-1) if pos[i] != pos[i+1]]  # 내부 gap i+1
        T = len(alt)
        if T < m: continue
        # T 개 교대 gap 중 정확히 m 개는 비우고, 나머지 T-m 개는 1개 이상, 다른 gap 은 자유
        free = gaps - T
        need = T - m
        ways = comb(T, m)
        # o 개의 1을 (need 개: >=1) + (free 개: >=0) 에 분배
        if o < need: continue
        rest = o - need
        ways *= comb(rest + need + free - 1, need + free - 1)
        tot += ways
    return tot
out['Q21'] = (q21((2, 5, 3), 3), q21_struct((2, 5, 3), 3))
out['T21'] = (q21((3, 4, 2), 2), q21_struct((3, 4, 2), 2))

# ---------- Q26 ----------
def q26(mult):
    a, b = symbols('a b', positive=True)
    kk = symbols('kk', integer=True, positive=True)
    # E(X)=b k, E(X^2)= b k(k+1)/2  ->  (k+1)/2 = mult
    K = 2*mult - 1
    H = sum(Rational(1, i) for i in range(1, K+1))
    V = b*K*(K+1)/2 - (b*K)**2
    bstar = solve(diff(V, b), b)[0]
    astar = 1 - bstar*H
    # 흔한 오답: 확률의 합을 a + b k = 1 로 잘못 둔 경우
    wrong_a = 1 - bstar*K
    return dict(k=K, H=H, b=bstar, a=astar, p_plus_q=fraction(astar)[0] + fraction(astar)[1], wrong_a=wrong_a)
out['Q26'] = q26(2)
out['T26'] = q26(3)

# ---------- Q28 ----------
def q28(f, coef):
    a, kk = symbols('a kk', real=True)
    g = f.subs(x, x - a)
    gp = diff(g, x)
    eqs = [gp.subs(x, kk), gp.subs(x, -kk), g.subs(x, kk) - g.subs(x, -kk)]
    sols = [s for s in solve(eqs, [a, kk], dict=True) if s[kk].is_positive]
    return [(s[a], s[kk], s[a] + coef*s[kk]**2) for s in sols]
out['Q28'] = q28(x*(x-1)**2*(x-2), 20)
out['T28'] = q28(x*(x-2)**2*(x-4), 10)

# ---------- Q29 ----------
def q29(balls, draws, target):
    S = lambda: [sum(c) for c in product(balls, repeat=draws)]
    num = den = 0
    for s in S():
        for u in S():
            if s > u:
                den += 1
                if s == target: num += 1
    fr = Fraction(num, den)
    return fr, fr.numerator + fr.denominator
out['Q29'] = q29((1, 2, 3), 2, 5)
out['T29'] = q29((1, 2, 3, 4), 2, 6)

# ---------- Q30 (경우 전수 + 수치 확인) ----------
def q30(B, m, lam):
    """f = B^{(x+a+b)/m} - a (x<=0), m log_B x - b (x>0); 근 집합 {0,a,b,c}, |c| = lam|b|"""
    found = []
    def roots_of(a_, b_):
        neg = lambda u: B**((u + a_ + b_)/m) - a_ - u
        pos = lambda u: m*mp.log(u, B) - b_ - u
        R = set()
        for lo, hi, fn in ((-200, 0, neg), (1e-9, 400, pos)):
            xs = [lo + (hi-lo)*i/40000 for i in range(40001)]
            for u, v in zip(xs, xs[1:]):
                if fn(u) == 0: R.add(round(u, 6))
                elif fn(u)*fn(v) < 0: R.add(round(float(mp.findroot(fn, (u, v), solver='bisect')), 6))
        if abs(neg(0)) < 1e-9: R.add(0.0)
        return sorted(R)
    # 경우 1: b>0 -> b 는 양의 근: m log_B b = 2b
    bs = set()
    for s in range(1, 4000):
        u, v = s/100, (s+1)/100
        h = lambda z: m*mp.log(z, B) - 2*z
        if h(u)*h(v) < 0 or h(u) == 0: bs.add(float(mp.findroot(h, (u, v), solver='bisect')) if h(u) != 0 else u)
    for b_ in bs:
        h = lambda z: m*mp.log(z, B) - z - b_
        for s in range(1, 40000):
            u, v = s/100, (s+1)/100
            if h(u)*h(v) < 0 or h(u) == 0:
                a_ = float(mp.findroot(h, (u, v), solver='bisect')) if h(u) != 0 else u
                found.append((a_, b_))
    # 경우 2: b<0 -> b 는 x<=0 쪽 근:  a B^{b/m} - a = b,  m log_B a = a + b
    for s in range(-4000, 0):
        u, v = s/100, (s+1)/100
        def r(bb):
            aa = bb/(B**(bb/m) - 1)
            return m*mp.log(aa, B) - aa - bb
        try:
            if r(u)*r(v) < 0:
                bb = float(mp.findroot(r, (u, v), solver='bisect'))
                found.append((bb/(B**(bb/m) - 1), bb))
        except Exception:
            pass
    ok = []
    for a_, b_ in found:
        R = roots_of(a_, b_)
        negs = [u for u in R if u < 0]
        rest = [u for u in R if abs(u) > 1e-6 and abs(u - a_) > 1e-4 and abs(u - b_) > 1e-4]
        if len(R) == 4 and len(negs) == 1 and len(rest) == 1 and 0.0 in R:
            c_ = rest[0]
            ok.append(dict(a=round(a_, 6), b=round(b_, 6), c=c_, roots=R, cond=abs(abs(c_) - lam*abs(b_)) < 1e-4))
    return ok
out['Q30'] = q30(3, 6, 2)
out['T30'] = q30(2, 4, 1)

# ---------- 보조: Q15, Q17, Q27 ----------
tt = symbols('tt', positive=True)
v1 = diff(tt**3 + 3*tt - 5, tt); v2 = 6
T15 = solve(Eq(v1, 5*v2), tt)
out['Q15'] = [diff(v1, tt).subs(tt, s) for s in T15]
f17 = Rational(1, 2)*x**2*(x + 1)
Qx = solve(Eq(3*x, -x/2 + 1), x)[0]
out['Q17'] = integrate(3*x - f17, (x, 0, 2)) - Rational(1, 2)*2*3*Qx
n = symbols('n', integer=True, positive=True)
an = 2*n - 1
Tn = Rational(1, 2)*4**an*(2**(an + 2) - 2**an)
S5 = summation(Tn, (n, 1, 5))
out['Q27'] = (simplify(Tn/8**an), nsimplify(S5/(2**30 - 1)), 2/(simplify(Tn/8**an)*nsimplify(S5/(2**30 - 1))))

for kq, v in out.items():
    print(kq, '=>', v)
