"""M1-13 검증 스크립트: 2026 수능 변별 문항(14,15,20,21,22,28,29,30) 정답·오답 경로·재사용 템플릿 수치 확인.
실행: python3 -I analysis/discrimination/scripts/2026-csat_verify.py  (sympy 필요)"""
import itertools, math
from fractions import Fraction as Fr
import sympy as sp
x, t, u = sp.symbols('x t u', real=True)

def hdr(s): print(f"\n=== {s} ===")

# ---------------------------------------------------------------- 14
def q14(AB, BC, ratio, cos_target=None, CG=None, verbose=True):
    """직각삼각형 ABC(∠B=90°), AD:DB=ratio, 원 중심 A 반지름 AD, E=원∩AC, |CG|=CG인 G(원 위). GH=2R·sin A."""
    AB, BC = sp.nsimplify(AB), sp.nsimplify(BC)
    AC = sp.sqrt(AB**2 + BC**2); r = AB*sp.Rational(ratio[0], sum(ratio))
    CE = AC - r
    if CG is None:
        CG = sp.sqrt(r**2 + AC**2 - 2*r*AC*cos_target)
    cosA_G = sp.simplify((r**2 + AC**2 - CG**2)/(2*r*AC))      # cos∠CAG
    EG = sp.sqrt(sp.simplify(2*r**2*(1 - cosA_G)))
    cosE = sp.simplify((CE**2 + EG**2 - CG**2)/(2*CE*EG))        # cos∠CEG
    sinE = sp.sqrt(sp.simplify(1 - cosE**2))
    R = sp.simplify(CG/(2*sinE))
    GH = sp.radsimp(2*R*BC/AC)
    if verbose: print(dict(AC=AC, r=r, CE=CE, CG=CG, cosCAG=cosA_G, EG=EG, cosCEG=cosE, sinCEG=sinE, R=R, GH=GH))
    return GH, R, sinE

hdr("14 원문")
GH, R, sinE = q14(3, 4, (2, 1), CG=2*sp.sqrt(6))
# 좌표 검증(그림 의존 없이): G 두 후보 모두 GH 동일
A = sp.Point(0, 0); E = sp.Point(sp.Rational(6, 5), sp.Rational(8, 5)); C = sp.Point(3, 4)
c_, s_ = sp.symbols('c s', real=True)
for sol in sp.solve([12*c_ + 16*s_ - 5, c_**2 + s_**2 - 1], [c_, s_]):
    G = sp.Point(2*sol[0], 2*sol[1])
    print("G", [sp.N(v, 6) for v in G], "GH =", sp.nsimplify(sp.simplify(2*sp.Circle(C, E, G).radius*sp.Rational(4, 5))))
print("선지:", [sp.Rational(6,5)*sp.sqrt(15), sp.Rational(38,25)*sp.sqrt(10), sp.Rational(14,5)*sp.sqrt(3), sp.Rational(32,25)*sp.sqrt(15), sp.Rational(8,5)*sp.sqrt(10)])
print("오답: 2R*cosA =", sp.radsimp(2*R*sp.Rational(3,5)), " R*sinA =", sp.radsimp(R*sp.Rational(4,5)), " 2R =", 2*R)
# 착각: CE=2로 두고 계산
CEw=2; EGw=sp.sqrt(6); CGw=2*sp.sqrt(6); cw=(CEw**2+EGw**2-CGw**2)/(2*CEw*EGw); Rw=CGw/(2*sp.sqrt(1-cw**2))
print("  CE를 AE(=2)로 착각: cos∠CEG =", sp.radsimp(cw), "(|cos|>1 → 삼각형 불성립, 스스로 오류 발견)")
hdr("14 템플릿: AB=4,BC=3, AD:DB=3:1, cos∠CAG=1/5")
q14(4, 3, (3, 1), cos_target=sp.Rational(1, 5))

# ---------------------------------------------------------------- 15
def q15(gl, gr, a_vals, fneg=-x**2, fpos=x**2 - x, p=1):
    """g = gl (x<-p), 0 (-p<=x<1), gr (x>=1); d = g - f. 극값 개수(부호 변화) 세기."""
    a = sp.Symbol('a', positive=True)
    res = {}
    for av in a_vals:
        pieces = [((-sp.oo, -p), (gl - fneg).subs(a, av)), ((-p, 0), (-fneg)), ((0, 1), (-fpos)), ((1, sp.oo), (gr - fpos).subs(a, av))]
        # 샘플링으로 부호 변화 세기 (구간 경계 포함)
        xs = [sp.Rational(k, 50) for k in range(-1500, 1501)]
        def d(xv):
            for (lo, hi), e in pieces:
                if lo <= xv < hi or (hi == sp.oo and xv >= lo): return e.subs(x, xv)
        signs = [sp.sign(d(xv)) for xv in xs]
        nz = [s for s in signs if s != 0]
        res[av] = sum(1 for i in range(1, len(nz)) if nz[i] != nz[i-1])
    return res
hdr("15 원문: a별 극값 개수")
a = sp.Symbol('a', positive=True)
print(q15(a*x + a, a*x - a, [1, 2, 3, sp.Rational(39, 10), 4, sp.Rational(41, 10), 5, 6]))
d_pos = (a*x - a) - (x**2 - x)
h3 = sp.integrate(x - x**2, (x, 0, 1)) + sp.integrate(d_pos.subs(a, 4), (x, 1, 3))
print("k=4, h(3) =", h3, " k+h(3) =", 4 + h3)
for kk in [2, 5]:
    hh = sp.integrate(x - x**2, (x, 0, 1)) + sp.integrate(d_pos.subs(a, kk), (x, 1, 3))
    print(f"  오답 k={kk}: k+h(3) =", kk + hh)
print("  오답 h(3)만:", h3, " 부호 반대(f-g):", 4 - h3, " [0,1] 부분 누락:", 4 + h3 - sp.Rational(1, 6))
hdr("15 템플릿: g = ax+2a (x<-2), 0 (-2<=x<1), ax-a (x>=1)")
print(q15(a*x + 2*a, a*x - a, [4, 7, 8, sp.Rational(81, 10), 9], p=2))
h3t = sp.integrate(x - x**2, (x, 0, 1)) + sp.integrate(d_pos.subs(a, 8), (x, 1, 3))
print("k=8, h(3) =", h3t, " k+h(3) =", 8 + h3t)

# ---------------------------------------------------------------- 20
def q20(alpha, P, a1, N=30):
    """S_n = alpha*a_n + P(n) (n>=2), a_1 주어짐. 일반항 생성 후 S_n 식 검증."""
    n = sp.Symbol('n')
    a2 = sp.solve(sp.Eq(a1 + u, alpha*u + P.subs(n, 2)), u)[0]
    seq = [None, sp.nsimplify(a1), a2]
    # a_{n+1} = alpha(a_{n+1}-a_n) + P(n+1)-P(n)
    for k in range(2, N):
        seq.append(sp.solve(sp.Eq(u, alpha*(u - seq[k]) + P.subs(n, k+1) - P.subs(n, k)), u)[0])
    ok = all(sp.simplify(sum(seq[1:k+1]) - (alpha*seq[k] + P.subs(n, k))) == 0 for k in range(2, N))
    return seq, ok
hdr("20 원문")
n = sp.Symbol('n')
seq, ok = q20(sp.Rational(2, 3), n**2/6 - n/6 + 10, 7)
print("a_1..a_12 =", seq[1:13], " S_n 식 성립:", ok)
print("2a_n+a_{n+1}=n 확인:", all(2*seq[k] + seq[k+1] == k for k in range(2, 20)), " n=1에서는", 2*seq[1] + seq[2])
val = sum(seq[1:13]) + sum(seq[2*k+1] for k in range(1, 6))
p_, q_, f12 = seq[2], val, sp.Rational(12, 3)
print("p=a2 =", p_, " q =", q_, " p*q/f(12) =", p_*q_/f12)
print("  오답: ㉠을 n=1에도 적용 → a2 =", 1 - 2*7, " → p*q/f(12) =", (1-2*7)*(7 + (1-2*7) + 35)/4,
      "; f(n)=n으로 착각 →", p_*q_/12)
hdr("20 템플릿: S_n = (3/4)a_n + n(n-1)/8 + 6, a1=5")
seq2, ok2 = q20(sp.Rational(3, 4), n*(n-1)/8 + 6, 5)
val2 = sum(seq2[1:13]) + 2*sum(seq2[2*k+1] for k in range(1, 6))
print("a1..a12 =", seq2[1:13], " 성립:", ok2, " a_{n+1}+3a_n=n:", all(seq2[k+1] + 3*seq2[k] == k for k in range(2, 20)))
print("p=a2 =", seq2[2], " q =", val2, " f(12)=12/4=3 → p*q/f(12) =", seq2[2]*val2/3)

# ---------------------------------------------------------------- 21
def q21(P, lam, Mmax=40, verbose=True):
    """f = c x(x-P)(x-beta), g = -f (x<t), f (x>=t). 분모 x(x-P).
    (나) 음수 m 집합 = {g(-1), lam*g(1)} (서로 다름). 모든 (t, beta) 경우를 기호적으로 탐색."""
    c, b = sp.symbols('c beta', real=True)
    f = c*x*(x - P)*(x - b)
    sols = []
    # t는 f의 근: 0, P, beta. beta 구간을 정수 경계로 나눠 각 구간에서 음수 집합을 결정
    cuts = list(range(-3, Mmax + 2))
    for tcase in ['0', 'P', 'beta']:
        for lo in cuts:
            for open_pt in [False, True]:     # 구간 (lo, lo+1) 내부 또는 정수점 beta=lo
                bt = sp.Rational(2*lo + 1, 2) if not open_pt else sp.Integer(lo)
                tv = {'0': 0, 'P': P, 'beta': bt}[tcase]
                # 극한값 lim_{x->m+} g/(x(x-P)) = s(m)*c*(m-beta), s=+1 if m>=t else -1
                N = [m for m in range(1, Mmax) if (1 if m >= tv else -1)*(m - bt) < 0]
                if not (1 <= len(N) <= 2) or (N and N[-1] >= Mmax - 2): continue
                g = lambda xv: (-f if xv < tv else f).subs(x, xv)
                e1, e2 = g(-1), lam*g(1)
                targets = [(N[0], N[0])] if len(N) == 1 else [(N[0], N[1]), (N[1], N[0])]
                for v1, v2 in targets:
                    for s in sp.solve([sp.Eq(e1, v1), sp.Eq(e2, v2)], [c, b], dict=True):
                        cv, bv = s[c], s[b]
                        if not (cv.is_real and cv > 0): continue
                        same_interval = (bv == bt) if open_pt else (lo < bv < lo + 1)
                        if tcase == 'beta' and not open_pt: pass
                        if same_interval:
                            sols.append((tcase, N, cv, bv, sp.simplify((g(-5)).subs({c: cv, b: bv}))))
    uniq = []
    for s_ in sols:
        if s_ not in uniq: uniq.append(s_)
    if verbose:
        for s_ in uniq: print("  t=%s N=%s c=%s beta=%s g(-5)=%s" % s_)
    return uniq
hdr("21 원문 (분모 x(x-2), lam=-7/2)")
sol21 = q21(2, sp.Rational(-7, 2))
# 단서 g(-1) != -7/2 g(1) 의 역할: 집합 원소 1개(N 크기 1)인 해가 존재하는지 위 탐색에 포함됨
print("  (위 목록에 |N|=1 해가 없으면 단서는 해를 줄이지 않는 안내용)")
hdr("21 템플릿 (분모 x(x-3), lam=-4, 답 g(-5))")
q21(3, -4)

# ---------------------------------------------------------------- 22
hdr("22 원문")
A_, B_ = sp.symbols('a b', positive=True)
lin = sp.solve([sp.Eq((A_ + 2*B_)/2, sp.Rational(77, 8)), sp.Eq((B_ + 2*A_)/2, sp.Rational(133, 8))], [A_, B_])
print("B=2A' 가정 연립:", lin, " 곡선1 위?", sp.simplify(sp.log(8*lin[A_] + 2, 16) - lin[B_]) == 0,
      " B=(2b,2a) 곡선2 위?", sp.simplify(4**(2*lin[B_] - 1) - sp.Rational(1, 2) - 2*lin[A_]) == 0,
      " a*b =", lin[A_]*lin[B_])
# 닮음 확인: 곡선1의 y=x 대칭 C1'(x)=2^(4x-3)-1/4,  2*C1'(x/2) = 곡선2?
C1p = 2**(4*x - 3) - sp.Rational(1, 4)
print("2*C1'(x/2) - (4^(x-1)-1/2) =", sp.simplify(2*C1p.subs(x, x/2) - (4**(x - 1) - sp.Rational(1, 2))))
# 중점 조건만으로 유일함: s(=B의 x좌표)에 대한 단조성
s = sp.Symbol('s', real=True)
F = sp.log(8*(sp.Rational(77, 4) - s) + 2, 16) + 4**(s - 1) - sp.Rational(1, 2) - sp.Rational(133, 4)
print("F'(s) 부호(양수면 단조증가):", [sp.N(sp.diff(F, s).subs(s, sv), 4) for sv in [0.6, 2, 3.5, 10, 19]], " 근:", sp.nsolve(F, s, 3))
print("직선 OB(y=9x)와 곡선2의 x>0 교점:", sp.nsolve(4**(x-1) - sp.Rational(1,2) - 9*x, x, 3.4), "(볼록-직선, x=0에서 곡선<직선 → 양의 교점 1개)")
hdr("22 템플릿: 곡선1 y=log_27(9x+3), 곡선2 y=3^(x-1)-1, 배율 3")
C1p_t = 3**(3*x - 2) - sp.Rational(1, 3)       # 곡선1의 y=x 대칭
print("3*C1'(x/3) - (3^(x-1)-1) =", sp.simplify(3*C1p_t.subs(x, x/3) - (3**(x - 1) - 1)))
at, bt_ = sp.Rational(26, 3), sp.Rational(4, 3)
print("A 곡선1 위?", sp.simplify(sp.log(9*at + 3, 27) - bt_) == 0, " B=(3b,3a)=", (3*bt_, 3*at), " 곡선2 위?", 3**(3*bt_ - 1) - 1 == 3*at,
      " 중점:", ((at + 3*bt_)/2, (bt_ + 3*at)/2), " a*b =", at*bt_)

# ---------------------------------------------------------------- 28
def boxes(k):
    if k % 2: return [1, 3, 5]
    return [d for d in range(1, 7) if k % d == 0]
def q28(nthrow, total_parity, event):
    num = den = 0
    for ks in itertools.product(range(1, 7), repeat=nthrow):
        bx = [0]*7
        for k in ks:
            for b in boxes(k): bx[b] += 1
        if sum(bx) % 2 == total_parity:
            den += 1; num += event(bx)
    return Fr(num, den), Fr(den, 6**nthrow)
hdr("28 원문")
print("P(조건부) , P(합 홀수) =", q28(4, 1, lambda bx: bx[3] == bx[2] + 1))
print("최대 사용 공 수(6만 4번):", 4*len(boxes(6)))
print("  오답: 조건부 무시(교집합 확률) =", Fr(5, 54), "; (Y,Z)=(1,0) 경우 누락 →", Fr(1,108)/Fr(40,81),
      "; 홀짝 필터 누락(교집합에 (0,1) 포함) →", (Fr(1,108)+Fr(1,12)+Fr(1,12))/Fr(40,81))
hdr("28 템플릿 후보")
print("합 짝수일 때 상자2 = 상자3:", q28(4, 0, lambda bx: bx[2] == bx[3])[0])
print("합 홀수일 때 상자1 = 상자2 + 2:", q28(4, 1, lambda bx: bx[1] == bx[2] + 2)[0])
print("합 짝수일 때 상자3 = 상자2 + 1:", q28(4, 0, lambda bx: bx[3] == bx[2] + 1)[0])
print("3번 반복, 합 홀수일 때 상자3 = 상자2 + 1:", q28(3, 1, lambda bx: bx[3] == bx[2] + 1)[0])

# ---------------------------------------------------------------- 29
hdr("29 원문")
aa = sp.Symbol('a')
p3 = aa/6*sp.Rational(sp.binomial(5, 3), 32) + (6 - aa)/6*sp.Rational(1, 8)
print("P(기록=3) =", sp.factor(p3))
av = sp.solve(sp.Eq(19200*p3, 4800), aa)[0]; pv = p3.subs(aa, av)
sig = sp.sqrt(19200*pv*(1 - pv)); z = (30*av)/sig
print("a =", av, " p =", pv, " sigma =", sig, " z =", z, " k = 0.5+0.477 =", 0.5 + 0.477, " 1000k =", 1000*(0.5 + 0.477))
print("  오답: 0.5 누락 → 477; 가중 없이 5번 던짐 확률만 → p =", sp.Rational(10, 32))
hdr("29 템플릿: a 이하 → 동전 4번, 초과 → 2번, 기록=2, n=1800")
p2 = aa/6*sp.Rational(sp.binomial(4, 2), 16) + (6 - aa)/6*sp.Rational(1, 4)
print("P(기록=2) =", sp.factor(p2))
av2 = sp.solve(sp.Eq(1800*p2, 600), aa)[0]; pv2 = p2.subs(aa, av2); sig2 = sp.sqrt(1800*pv2*(1 - pv2))
print("a =", av2, " p =", pv2, " sigma =", sig2, " P(X<=600+5a): z =", 5*av2/sig2, "→ 0.5+0.341 → 1000k =", 841)
print("모비율 변형: n=1800, p̂=X/n, P(p̂ >= 1/3 - a/180): z =", sp.simplify((pv2 - (pv2 - av2/180))/sp.sqrt(pv2*(1-pv2)/1800)))

# ---------------------------------------------------------------- 30
def q30(npocket, nball, ones_allowed, need_both_neighbors=False):
    cnt = {}
    for v in itertools.product(range(3), repeat=npocket):
        if sum(v) != nball: continue
        ok = True
        for i in range(npocket):
            if v[i] == 2:
                L = v[i-1] if i > 0 else (None if need_both_neighbors else 0)
                R_ = v[i+1] if i < npocket - 1 else (None if need_both_neighbors else 0)
                if L is None or R_ is None or L or R_: ok = False; break
        if ok:
            o = v.count(1); cnt[o] = cnt.get(o, 0) + 1
    return cnt, sum(cnt.get(o, 0) for o in ones_allowed)
hdr("30 원문")
c30, ans30 = q30(10, 8, (4, 6)); print("1인 주머니 수별 경우:", dict(sorted(c30.items())), " 답(4 또는 6):", ans30)
print("  오답: 양끝의 2 불허(양옆 모두 있어야 한다고 오해) →", q30(10, 8, (4, 6), need_both_neighbors=True)[1],
      "; 한 경우만:", c30[4], c30[6])
# 틈(gap) 방법 검산
def gap_count(ones, zeros, twos):
    tot = 0
    for arr in set(itertools.permutations([1]*ones + [0]*zeros)):
        ext = ['W'] + list(arr) + ['W']
        good = sum(1 for i in range(len(ext) - 1) if ext[i] in ('W', 0) and ext[i+1] in ('W', 0))
        tot += math.comb(good, twos)
    return tot
print("틈 방법: (1이 6개)", gap_count(6, 3, 1), " (1이 4개)", gap_count(4, 4, 2))
hdr("30 템플릿: 주머니 9개, 공 7개, 1인 주머니 3개 또는 5개")
c30t, ans30t = q30(9, 7, (3, 5)); print(dict(sorted(c30t.items())), "답:", ans30t)
