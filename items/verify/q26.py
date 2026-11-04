"""q26 검증: 모비율의 추정 — 표본비율 p̂의 분포 (단답, 정답 98).

표본비율 p̂ = X/n, X ~ B(n, p). 모든 기댓값은 이항분포 확률질량함수를
직접 합해서(공식 E(p̂)=p, V(p̂)=p(1-p)/n 을 쓰지 않고) 계산한다.
  (가) Σ_{k=0}^{n} (n-k) P(p̂=k/n) = 12
  (나) Σ_{k=0}^{n} k^2   P(p̂=k/n) = 40
  묻는 값: Σ_{k=0}^{n} k(n-k)/n^2 · P(p̂=k/n) = b/a (서로소) → a+b
"""
import sys
from fractions import Fraction as F
from math import comb, gcd

fails = []
def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {info}" if info else ""))
    if not ok:
        fails.append(name)

def pmf(n, p):
    return [comb(n, k) * p**k * (1 - p)**(n - k) for k in range(n + 1)]

def S(n, p, g):
    return sum(g(k) * w for k, w in enumerate(pmf(n, p)))

A = lambda n: (lambda k: n - k)          # (가)
B = lambda n: (lambda k: k * k)          # (나)
T = lambda n: (lambda k: F(k * (n - k), n * n))  # 묻는 값

# 다항식(계수 리스트, 낮은 차수부터) 연산 — 이항분포 합을 p의 다항식으로 정확히 전개
def padd(a, b):
    r = [F(0)] * max(len(a), len(b))
    for i, c in enumerate(a): r[i] += c
    for i, c in enumerate(b): r[i] += c
    return r
def pmul(a, b):
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return r
def ppow(a, e):
    r = [F(1)]
    for _ in range(e): r = pmul(r, a)
    return r
def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0: a.pop()
    return a
def sym_sum(n, g):
    tot = [F(0)]
    for k in range(n + 1):
        term = pmul(ppow([F(0), F(1)], k), ppow([F(1), F(-1)], n - k))
        tot = padd(tot, [F(g(k) * comb(n, k)) * c for c in term])
    return trim(tot)
def real_roots_01(poly):
    """poly 차수 ≤ 2 의 (0,1) 안 실근 (float 또는 Fraction)."""
    poly = trim(poly)
    if len(poly) == 2:
        r = -poly[0] / poly[1]; return [r] if 0 < r < 1 else []
    if len(poly) == 3:
        c, b, a = poly; D = b * b - 4 * a * c
        if D < 0: return []
        rs = {(-b + s * float(D) ** 0.5) / (2 * a) for s in (1, -1)}
        return [r for r in rs if 0 < r < 1]
    raise ValueError(poly)

# (a)(b) 정답·유일성: n=1..NMAX 전수. (가)의 합을 p의 다항식으로 전개해 근을 구하고, 그 p로 (나)를 정확히 확인
NMAX = 100
sols = []
for n in range(1, NMAX + 1):
    eqA = padd(sym_sum(n, A(n)), [F(-12)])
    assert len(trim(eqA)) <= 2  # (가)는 p의 1차식
    for r in real_roots_01(eqA):
        if S(n, r, A(n)) == 12 and S(n, r, B(n)) == 40:
            sols.append((n, r))
check("(a)(b) 조건 만족 (n,p) 유일 (n≤100 전수)", sols == [(18, F(1, 3))], str(sols))

# n>100 꼬리: (가)에서 p=(n-12)/n. 이항 직접 합(부동소수)으로 (나)의 값이 40보다 큼을 확인
tail_ok = all(sum(k*k*w for k, w in enumerate(pmf(nn, (nn-12)/nn))) > 40 for nn in range(101, 1001))
check("n=101..1000에서 (가)를 만족하면 (나)의 합 > 40", tail_ok)

n, p = 18, F(1, 3)
val = S(n, p, T(n))
check("묻는 값 = 17/81 (이항 직접 합)", val == F(17, 81), str(val))
ans = val.numerator + val.denominator
check("정답 98, 1~999 자연수", ans == 98 and 1 <= ans <= 999, str(ans))

# 기호 풀이 대조: m=np 에 대해 m^3+12m^2-28m-480 = (m-6)(m^2+18m+80), 뒤 인수의 판별식<0? 근 -8,-10(음수)
check("기호: np의 양의 근은 6뿐", pmul([F(-6), F(1)], [F(80), F(18), F(1)]) == [F(-480), F(-28), F(12), F(1)]
      and 18**2 - 4*80 >= 0 and all(r < 0 for r in (-8, -10)))

# (c) 조건 필요성
#  (가) 제거: (나)만 → 여러 (n,p)
onlyB = []
for nn in range(1, 80):
    eqB = padd(sym_sum(nn, B(nn)), [F(-40)])
    for r in real_roots_01(eqB):
        r = float(r)
        assert abs(sum(k*k*w for k, w in enumerate(pmf(nn, r))) - 40) < 1e-6
        onlyB.append((nn, round(sum(k*(nn-k)/nn**2*w for k, w in enumerate(pmf(nn, r))), 6)))
check("(가) 제거 → 해 여러 개, 답 여러 값", len(onlyB) > 1 and len({v for _, v in onlyB}) > 1, f"{len(onlyB)}개 해, 예: {onlyB[:3]}")
#  (나) 제거: (가)만 → n(1-p)=12, n≥13 모두
onlyA = [(nn, F(nn - 12, nn)) for nn in range(13, 40)]
assert all(S(nn, pp, A(nn)) == 12 for nn, pp in onlyA)
valsA = {S(nn, pp, T(nn)) for nn, pp in onlyA}
check("(나) 제거 → 해 여러 개, 답 여러 값", len(valsA) > 1, f"{len(onlyA)}개 해")

# (d) 대표 오답 경로 값 (정답과 겹치지 않음)
wrong = {}
# W1: 묻는 값을 E(p̂)E(1-p̂)=p(1-p) 로 처리(분산 항 누락) → 2/9 → 11
w = p * (1 - p); wrong["W1 p(1-p)"] = w.numerator + w.denominator
# W2: E(p̂^2)만 구하고 멈춤 → 10/81 → 91
w = S(n, p, lambda k: F(k * k, n * n)); wrong["W2 E(p̂^2)"] = w.numerator + w.denominator
# W3: V(p̂)=p(1-p)/n^2 로 오기 → E(p̂^2)=p^2+pq/n^2 → 323/1458 → 1781 (범위 밖)
w = p - (p * p + p * (1 - p) / n**2); wrong["W3 V/n^2"] = w.numerator + w.denominator
# W4: (나)를 n^2p^2=40 으로(분산 누락) → np=√40, n=12+√40 비자연수 → 진행 불가
wrong["W4 (나) 분산 누락"] = "n=12+2√10 (자연수 아님)"
for k_, v in wrong.items():
    print("  오답", k_, "→", v)
check("오답 값이 정답 98과 다름", all(v != 98 for v in wrong.values()))

print()
if fails:
    print("실패:", fails); sys.exit(1)
print("모두 통과: 정답 98 (n=18, p=1/3, 묻는 값 17/81)")
