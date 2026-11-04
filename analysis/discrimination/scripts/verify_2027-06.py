"""2027학년도 6월 모평 변별 문항 검증 스크립트 (analysis/discrimination/2027-06.md 부록).
실행: python3 analysis/discrimination/scripts/verify_2027-06.py   (sympy 필요)
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
import numpy as np
import sympy as sp

x, t, th = sp.symbols('x t theta', real=True)

# ---------------- 14 ----------------
def roots14(a, b, f1=sp.Rational(1, 2), c=None):
    """0<=x<=2 에서 (cos(bπx)-f1)(a cos(bπx)+(a+2)/2)=0 의 서로 다른 실근 개수 (θ=bπx 로 치환, 정확 계산)."""
    if c is None:
        c = -sp.Rational(1, 2) - 1 / sp.nsimplify(a)
    I = sp.Interval(0, 2 * b * sp.pi)
    s = sp.solveset(sp.cos(th) - f1, th, I) | sp.solveset(sp.cos(th) - c, th, I)
    return len(s)

sols14 = []
for b in range(1, 11):
    for a in [sp.Rational(k, 4) for k in range(1, 25)]:
        if roots14(a, b) == 15:
            sols14.append((a, b))
print('14 해(a=k/4, 1<=b<=10 탐색):', sols14, '-> a+b =', [a + b for a, b in sols14])
# 음수 a 허용 시 가능한 개수 (단서 '양수 a'의 역할)
print('14 a<0 허용 시 b=5 개수 예:', {a: roots14(a, 5) for a in [-1, sp.Rational(-2, 3), sp.Rational(-1, 2), -2]})

# 14 템플릿: (cos(bπx)+1/2)(a cos(bπx) - (a+3)/2)=0, 0<=x<=2, 개수 13
def roots14T(a, b):
    I = sp.Interval(0, 2 * b * sp.pi)
    c = (sp.nsimplify(a) + 3) / (2 * sp.nsimplify(a))
    return len(sp.solveset(sp.cos(th) + sp.Rational(1, 2), th, I) | sp.solveset(sp.cos(th) - c, th, I))
solT = [(a, b) for b in range(1, 11) for a in [sp.Rational(k, 4) for k in range(1, 25)] if roots14T(a, b) == 13]
print('14T 해:', solT)

# ---------------- 15 ----------------
k = sp.symbols('k', positive=True)
f15 = k * x**2 * (x - 3)
fmin = sp.minimum(f15, x, sp.Interval(0, 3))
ksol = sp.solve(sp.Eq(-fmin, 1), k)
print('15 [0,3] 최솟값:', fmin, ' k =', ksol, ' f(6) =', f15.subs(k, ksol[0]).subs(x, 6))

def sign_change_set(fn, lo, hi, L, grid):
    """∫_p^{p+L}|f| != |∫ f| 인 p (= (p,p+L)에서 f 부호 변화) 를 grid 위에서 판정."""
    out = []
    for p in grid:
        xs = [p + L * i / 400 for i in range(1, 400)]
        vals = [fn(v) for v in xs]
        if min(vals) < -1e-12 and max(vals) > 1e-12:
            out.append(p)
    return out

f15n = sp.lambdify(x, sp.Rational(1, 4) * x**2 * (x - 3))
ps = sign_change_set(f15n, -5, 8, 3, [i / 20 for i in range(-100, 160)])
print('15 (가) p 범위(수치):', min(ps), '~', max(ps))
qs = [q / 100 for q in range(-200, 300) if
      (lambda q: (lambda v: min(v) < -1e-12 and max(v) > 1e-12)([f15n(3 * i / 600) + q for i in range(1, 600)]))(q / 100)]
print('15 (나) q 범위(수치):', min(qs), '~', max(qs))
# 15 템플릿: f=kx^2(x-6), 창 길이 5, (가) 1<p<6, (나) ∫_0^6 → 0<q<8, f(8)?
fT = k * x**2 * (x - 6)
kT = sp.solve(sp.Eq(-sp.minimum(fT, x, sp.Interval(0, 6)), 8), k)
fTn = sp.lambdify(x, fT.subs(k, kT[0]))
psT = sign_change_set(fTn, -5, 12, 5, [i / 20 for i in range(-100, 240)])
qsT = [q / 10 for q in range(-50, 150) if
       (lambda q: (lambda v: min(v) < -1e-12 and max(v) > 1e-12)([fTn(6 * i / 600) + q for i in range(1, 600)]))(q / 10)]
print('15T k =', kT, ' (가) p:', min(psT), '~', max(psT), ' (나) q:', min(qsT), '~', max(qsT), ' f(8) =', fT.subs(k, kT[0]).subs(x, 8))

# ---------------- 20 ----------------
def check20(n):
    m = n
    beta = sp.Integer(m) ** sp.Rational(1, n + 1)
    alpha = beta / m
    b = alpha ** (-1 / beta)
    # 검산: β=b^α, β=-log_b α, αβ^n=1
    ok = [sp.N(b ** alpha - beta), sp.N(-sp.log(alpha) / sp.log(b) - beta), sp.simplify(alpha * beta**n - 1)]
    r = beta / (-1 + sp.Rational(1, n + 1))
    gm = -sp.log(m) / sp.log(b)
    return dict(p=m, q=beta, r=sp.simplify(r), r_check=sp.N(gm - r), b=sp.N(b), checks=ok,
                pqr=sp.simplify(m * beta * r))
c20 = check20(3)
print('20 n=3:', c20, ' (pqr)^2 =', sp.simplify(c20['pqr'] ** 2))
c20T = check20(2)
print('20T n=2:', c20T, ' (pqr)^3 =', sp.simplify(c20T['pqr'] ** 3))

# ---------------- 21 ----------------
def G_maxroot(fc, kval):
    coeffs = [float(cf) for cf in sp.Poly(fc, x).all_coeffs()]
    coeffs[-1] -= kval
    rr = np.roots(coeffs)
    return max(z.real for z in rr if abs(z.imag) < 1e-6)

a_, b_, c_ = sp.symbols('a b c')
f21 = x**3 + a_ * x**2 + b_ * x + c_
h21 = sp.expand(sp.diff(f21, x).subs(x, t) - 4 * t**2 + 4)
print('21 h(t) =', h21)
sol21 = sp.solve([sp.diff(h21, t).subs(t, 3),               # 꼭짓점 t=3
                  sp.diff(f21, x).subs(x, 1),                 # 극소점 x=1
                  h21.subs(t, 3) - f21.subs(x, 1)], [a_, b_, c_], dict=True)
f21s = sp.expand(f21.subs(sol21[0]))
print('21 f =', sp.expand(f21s), ' f(2) =', f21s.subs(x, 2))
h21s = sp.lambdify(t, h21.subs(sol21[0]))
ts = [i / 1000 for i in range(-2000, 8001)]
gs = [G_maxroot(f21s, h21s(tt)) for tt in ts]
jumps = [(ts[i], round(gs[i], 3), round(gs[i + 1], 3)) for i in range(len(ts) - 1) if abs(gs[i + 1] - gs[i]) > 0.05]
print('21 수치 점프 위치:', jumps, ' g(3)=', round(G_maxroot(f21s, h21s(3)), 6))

# 21 템플릿: h(t)=f'(t)-4t^2+4, t=2에서만 불연속, g(2)=3
solT21 = sp.solve([sp.diff(h21, t).subs(t, 2), sp.diff(f21, x).subs(x, 3), h21.subs(t, 2) - f21.subs(x, 3)], [a_, b_, c_], dict=True)
fT21 = sp.expand(f21.subs(solT21[0])); hT = sp.lambdify(t, h21.subs(solT21[0]))
gsT = [G_maxroot(fT21, hT(tt)) for tt in ts]
jT = [(ts[i], round(gsT[i], 3), round(gsT[i + 1], 3)) for i in range(len(ts) - 1) if abs(gsT[i + 1] - gsT[i]) > 0.05]
print('21T f =', sp.expand(fT21), ' f(1) =', fT21.subs(x, 1), ' 점프:', jT, ' g(2)=', round(G_maxroot(fT21, hT(2)), 6))

# ---------------- 22 ----------------
def seq22(N, seeds, rules):
    a = dict(seeds)
    for n in range(1, N):
        if n in a:
            continue
        a[n] = rules(n, a)
    return a

def r22(n, a):
    if n % 2 == 0:
        return a[n // 2] + 1
    return a[(n - 1) // 4] + 4 if n % 4 == 1 else a[(n - 3) // 4] + 4

A = seq22(1 << 14, {1: 1, 3: 4}, r22)
ks = [kk for kk in A if A[kk] == 10]
print('22 개수 =', len(ks), ' 최대 k =', max(ks), ' (k>=4096 에서 최소값', min(A[kk] for kk in A if kk >= 4096), ')')

@lru_cache(None)
def N(s, w4=2):
    if s < 0:
        return 0
    if s == 0:
        return 1
    return N(s - 1, w4) + w4 * N(s - 4, w4)
print('22 점화 N(9)+N(6) =', N(9) + N(6), ' | 씨앗 3 누락:', N(9), ' | 4n+1/4n+3 한 가지로 셈:', N(9, 1) + N(6, 1))

# 22 템플릿: a1=2,a2=3, a_{3n}=a_n+1, a_{3n+1}=a_{3n+2}=a_n+3 (n>=1), a_k=9 개수
def rT(n, a):
    return a[n // 3] + 1 if n % 3 == 0 else a[n // 3] + 3
AT = seq22(3 ** 9, {1: 2, 2: 3}, rT)
print('22T 개수 =', sum(1 for kk in AT if AT[kk] == 9), ' 최대 k =', max(kk for kk in AT if AT[kk] == 9))

# ---------------- 28 ----------------
def flips(kd, rule):
    if rule == 'orig':
        return {i for i in range(1, 7) if (kd % 2 and i <= kd) or (kd % 2 == 0 and i >= kd)}
    if rule == 'strict':
        return {i for i in range(1, 7) if (kd % 2 and i < kd) or (kd % 2 == 0 and i > kd)}

def prob28(rolls=4, rule='orig', back=(1, 6), target_front=True):
    cnt = 0
    for seq in product(range(1, 7), repeat=rolls):
        state = {i: (i in back) for i in range(1, 7)}   # True = 뒷면
        for kd in seq:
            for i in flips(kd, rule):
                state[i] = not state[i]
        ok = (not any(state.values())) if target_front else all(state.values())
        cnt += ok
    return F(cnt, 6 ** rolls), cnt
print('28 정답:', prob28())
print('28 변형: 3회', prob28(3), ' 5회', prob28(5), ' 미만/초과', prob28(rule='strict'), ' 모두 뒷면', prob28(target_front=False))
# 28 손풀이 식: (구간 선택 수열 20) x (짝수 눈 홀수 번 8) / 6^4
print('28 손풀이:', F(20 * 8, 6 ** 4))
# 28 템플릿: 처음에 1,4,5 가 뒷면, 3회 (손풀이: 3! x (짝수 눈 0 또는 2번: 4) = 24)
print('28T (뒷면 1,4,5 / 3회):', prob28(3, back=(1, 4, 5)), ' 손풀이', F(6 * 4, 6 ** 3))

# ---------------- 29 ----------------
def p29(nd, s):
    tot = 3 ** nd
    good = sum(1 for d in product([1, 3, 5], repeat=nd) if sum(d) == s)
    return F(good, tot), good
pr, g = p29(5, 15)
print('29:', pr, g, ' p+q =', pr.numerator + pr.denominator)
print('29 오답: 상한 무시 C(9,5)/243 =', F(comb(9, 5), 243), '->', F(comb(9, 5), 243).numerator + F(comb(9, 5), 243).denominator,
      '| 조건부 무시 51/6^5 =', F(51, 6 ** 5), '->', F(51, 6**5).numerator + F(51, 6**5).denominator)
prT, gT = p29(4, 12)
print('29T (4개, 합 12):', prT, gT, ' p+q =', prT.numerator + prT.denominator)

# ---------------- 30 ----------------
def count30(y, p, b, forbid=('Y', 'P')):
    @lru_cache(None)
    def f(y, p, b, last):
        if y == p == b == 0:
            return 1
        tot = 0
        for col, rem in (('Y', y), ('P', p), ('B', b)):
            if rem == 0:
                continue
            if {last, col} == set(forbid) and last != col:
                continue
            tot += f(y - (col == 'Y'), p - (col == 'P'), b - (col == 'B'), col)
        return tot
    return f(y, p, b, '')
slot = sum(sp.factorial(5) / (sp.factorial(i) * sp.factorial(j) * sp.factorial(5 - i - j)) * comb(3, i - 1) * comb(3, j - 1)
           for i in range(1, 5) for j in range(1, 5) if i + j <= 5)
word = sum(n_d * comb(12 - d, 4 - d) for d, n_d in [(1, 2), (2, 6), (3, 18), (4, 18)])
print('30 DP =', count30(4, 4, 4), ' 칸 방법 =', slot, ' 단어 방법 =', word)
print('30 오답: 빈 칸 불허(모든 칸 사용) =', sum(sp.factorial(5) / (sp.factorial(i) * sp.factorial(j)) * comb(3, i - 1) * comb(3, j - 1)
                                     for i in range(1, 5) for j in range(1, 5) if i + j == 5),
      '| 전체 12!/(4!)^3 =', sp.factorial(12) / sp.factorial(4) ** 3)
print('30T (3,3,3):', count30(3, 3, 3), ' (4,4,3):', count30(4, 4, 3), ' (3,3,4):', count30(3, 3, 4))
