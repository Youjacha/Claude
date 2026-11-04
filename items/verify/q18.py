"""q18 검증 스크립트 (미적분Ⅰ · 함수의 극한 존재 조건).

문항: 최고차항의 계수가 1인 삼차함수 f(x)가
  (가) lim_{x->t} f(x)/(x^2-t^2) 의 값이 존재하도록 하는 실수 t의 개수는 1
  (나) lim_{x->0} f(x)/x 의 값이 존재
  (다) lim_{x->inf} (f(x)-x^3)/x^2 = -4
를 만족시킬 때 f(5)의 값. 정답 ② 45.

검사: (0) 극한 판정 규칙을 sympy.limit로 독립 확인, (a) 정답, (b) 유일성(기호 + 전수),
(c) 조건 필요성, (d) 선지(등간격·정답 ②·오답 경로 값).
"""
import random
import sys
from fractions import Fraction

import sympy as sp

x, t = sp.symbols("x t", real=True)
FAILS = []


def check(cond, msg):
    print(("  PASS  " if cond else "  FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def lim_exists(expr, a):
    """x -> a 의 양쪽 극한이 유한하고 같은지 sympy.limit로 직접 판정."""
    try:
        lp = sp.limit(expr, x, a, "+")
        lm = sp.limit(expr, x, a, "-")
    except Exception:
        return False
    return lp.is_finite and lm.is_finite and sp.simplify(lp - lm) == 0


def A_by_limits(f):
    """(가)의 집합 A를 극한 계산으로 구한다.
    t가 f의 근도 0도 아니면 분자 -> f(t) != 0, 분모 -> 0 이므로 극한이 없다(아래에서 표본 확인).
    따라서 후보 t = f의 실근 ∪ {0} 에서만 sympy.limit로 판정한다."""
    cands = set(sp.Poly(f, x).real_roots()) | {sp.Integer(0)}
    return {c for c in cands if lim_exists(f / (x**2 - c**2), c)}


def A_rule(coeffs):
    """판정 규칙(해설의 [번역]): A = {f의 0이 아닌 서로 다른 실근} ∪ ({0} if x^2 | f)."""
    b, c, d = coeffs
    f = sp.Poly(x**3 + b * x**2 + c * x + d, x)
    roots = {r for r in f.real_roots() if r != 0}
    return len(roots) + (1 if (c == 0 and d == 0) else 0)


def cond_ga(coeffs):
    return A_rule(coeffs) == 1


def cond_na(coeffs):
    return coeffs[2] == 0          # lim f(x)/x 존재 <=> f(0)=0


def cond_da(coeffs):
    return coeffs[0] == -4         # lim (f-x^3)/x^2 = b


def F(coeffs):
    b, c, d = coeffs
    return x**3 + b * x**2 + c * x + d


print("[0] 판정 규칙을 sympy.limit로 독립 확인")
random.seed(18)
samples = [(-4, 4, 0), (-4, 0, 0), (0, 0, 0), (-4, 5, 0), (-4, 3, 0), (-6, 9, 0),
           (-4, sp.Rational(16, 3), sp.Rational(-64, 27))]
# 근이 정확히 표현되는 무작위 표본: 세 정수근(중복·0 포함) 또는 정수근 × 실근 없는 이차식
for _ in range(20):
    rs = [random.choice([0, 0, 1, -1, 2, -2, 3]) for _ in range(3)]
    samples.append(tuple(sp.Poly(sp.prod([x - r for r in rs]), x).all_coeffs()[1:]))
for _ in range(8):
    r, p0 = random.randint(-3, 3), random.randint(-3, 3)
    q0 = p0 * p0 + random.randint(1, 4)          # x^2+2p0x+q0, 판별식 < 0
    samples.append(tuple(sp.Poly((x - r) * (x**2 + 2 * p0 * x + q0), x).all_coeffs()[1:]))
ok = True
for co in samples:
    f = F(co)
    if len(A_by_limits(f)) != A_rule(co):
        ok = False
        print("    mismatch", co, A_by_limits(f), A_rule(co))
    # 근도 0도 아닌 t 하나에서 극한이 없음을 확인
    tt = 7 + random.random()
    tt = sp.Rational(int(tt * 100), 100)
    if f.subs(x, tt) != 0:
        ok = ok and not lim_exists(f / (x**2 - tt**2), tt)
check(ok, f"표본 {len(samples)}개에서 |A|(sympy.limit) = |A|(규칙)")
check(not lim_exists(x * (x - 2)**2 / x**2, 0), "f=x(x-2)^2: t=0에서 극한 없음 (0은 단순근)")
check(lim_exists(x**2 * (x - 4) / x**2, 0), "f=x^2(x-4): t=0에서 극한 존재 (값 -4)")
d_ = sp.symbols("d", real=True)
check(lim_exists((x**3 - 4 * x**2 + 3 * x) / x, 0) and not lim_exists((x**3 - 4 * x**2 + 3 * x + 1) / x, 0),
      "(나) f(0)=0이면 존재, f(0)!=0이면 없음")
b_, c_ = sp.symbols("b c", real=True)
check(sp.limit((x**3 + b_ * x**2 + c_ * x + d_ - x**3) / x**2, x, sp.oo) == b_, "(다) 극한값 = x^2의 계수 b")

print("[a] 정답")
fstar = x * (x - 2)**2
co_star = tuple(int(v) for v in sp.Poly(fstar, x).all_coeffs()[1:])
check(co_star == (-4, 4, 0), f"f = x(x-2)^2 = x^3-4x^2+4x, 계수 {co_star}")
check(A_by_limits(fstar) == {2}, f"A = {A_by_limits(fstar)} (원소 1개)")
check(lim_exists(fstar / x, 0), "(나) 성립")
check(sp.limit((fstar - x**3) / x**2, x, sp.oo) == -4, "(다) 성립")
ans = fstar.subs(x, 5)
check(ans == 45, f"f(5) = {ans}")

print("[b] 유일성")
# 기호: (나) d=0, (다) b=-4 => f = x(x^2-4x+c). c=0 => A={0,4}; c!=0 => A = x^2-4x+c의 실근(0 아님)
c = sp.symbols("c", real=True)
disc = sp.discriminant(x**2 - 4 * x + c, x)
check(sp.solve(sp.Eq(disc, 0), c) == [4], "판별식 16-4c = 0 <=> c = 4 (c<4: 근 2개, c>4: 근 0개)")
check(A_rule((-4, 0, 0)) == 2, "c=0 (f=x^2(x-4)): |A| = 2 → 제외")
# 전수 1: (나)(다) 아래 c를 -40..40, 1/4 간격
sols = [cv for cv in (Fraction(k, 4) for k in range(-160, 161))
        if cond_ga((-4, sp.Rational(cv.numerator, cv.denominator), 0))]
check(sols == [Fraction(4)], f"c ∈ [-40,40] (1/4 간격) 전수: 해 {sols}")
# 전수 2: 정수 b,c,d ∈ [-8,8] 모든 단최고차 삼차식
allsol = [co for co in ((b, cc, dd) for b in range(-8, 9) for cc in range(-8, 9) for dd in range(-8, 9))
          if cond_na(co) and cond_da(co) and cond_ga(co)]
check(allsol == [(-4, 4, 0)], f"정수 계수 [-8,8]^3 전수: 해 {allsol}")

print("[c] 조건 필요성 (하나씩 빼면 f(5)가 둘 이상)")
grid = [(b, cc, dd) for b in range(-8, 9) for cc in range(-12, 13) for dd in range(-12, 13)]
grid += [(-4, sp.Rational(16, 3), sp.Rational(-64, 27))]  # (x-4/3)^3
for name, conds in [("(가) 제외", (cond_na, cond_da)),
                    ("(나) 제외", (cond_ga, cond_da)),
                    ("(다) 제외", (cond_ga, cond_na))]:
    vals = sorted({F(co).subs(x, 5) for co in grid if all(cd(co) for cd in conds)}, key=float)
    check(len(vals) >= 2, f"{name}: f(5) 후보 {len(vals)}개, 예 {[str(v) for v in vals[:4]]}")

print("[d] 선지")
options = [25, 45, 65, 85, 105]
check(options.index(45) == 1, "정답 45는 ②")
check(len(set(options)) == 5 and len({options[i + 1] - options[i] for i in range(4)}) == 1, "등간격 오름차순(간격 20)")
w1 = (x**2 * (x - 4)).subs(x, 5)            # t=0 점검 누락: c=0인 x^2(x-4)를 |A|=1로 오판
w2 = ((x - sp.Rational(4, 3))**3).subs(x, 5)  # (나) 무시, '실근 하나' = 삼중근으로 처리
w3 = (x * (x + 2)**2).subs(x, 5)            # (다)에서 -2r=-4의 부호 실수 r=-2
w4 = (x * (x - 4)**2).subs(x, 5)            # x(x-r)^2의 x^2 계수를 -r로 착각 r=4
check(w1 == 25 and options.index(25) == 0, f"오답 경로 W1 (t=0 누락) = {w1} → ①")
check(not w2.is_integer, f"오답 경로 W2 (삼중근) = {w2} → 비정수, 선지 밖")
check(w3 == 245 and w3 not in options, f"오답 경로 W3 (부호) = {w3} → 선지 밖")
check(w4 == 5 and w4 not in options, f"오답 경로 W4 (계수 착각) = {w4} → 선지 밖")
check(all(w != 45 for w in (w1, w2, w3, w4)), "오답 경로 값이 정답과 겹치지 않음")

print()
if FAILS:
    print(f"FAILED {len(FAILS)}")
    sys.exit(1)
print("ALL PASS — q18 정답 ② 45")
