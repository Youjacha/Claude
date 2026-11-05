"""M1-8에서 바뀐 문항 독립 재계산(3차 검수): q6, q15, q16, q20, q27. 해설·verify를 보지 않고 본문만으로."""
import sympy as sp
from fractions import Fraction as F
import math
# q6: n=400, p̂=0.2, 95%
L = 2 * 1.96 * math.sqrt(0.2 * 0.8 / 400); print("q6 b-a =", round(L, 4)); assert abs(L - 0.0784) < 1e-12
# q15: v=4(t-1)(t-3)(t-r), (나)로 r∈{1,3}(r≤0, 1<r<3, r>3은 방향 전환 2·3회) — 전수로 확인
t, r = sp.symbols('t r')
def sign_changes(rv):
    v = 4*(t-1)*(t-3)*(t-rv); xs = [sp.Rational(k, 50) for k in range(1, 400)]
    s = [sp.sign(v.subs(t, x)) for x in xs]; s = [q for q in s if q != 0]
    return sum(1 for i in range(len(s)-1) if s[i] != s[i+1])
cand = [rv for rv in [sp.Rational(k, 4) for k in range(-8, 30)] if sign_changes(rv) == 1]
ok = []
for rv in cand:
    v = 4*(t-1)*(t-3)*(t-rv); x2 = sp.integrate(v, (t, 0, 2)); v2 = v.subs(t, 2)
    if x2 * v2 < 0: ok.append(rv)          # (다) 원점을 향함: 위치와 속도 부호 반대
print("q15 (나) 후보 r =", cand, " (다) 통과 r =", ok)
assert ok == [3]; acc = sp.diff(4*(t-1)*(t-3)**2, t).subs(t, 4); print("q15 a(4) =", acc); assert acc == 28
# q16: a,k 자연수, 0≤x≤2π 에서 근 개수 수치 전수(a≤30, k=1..3)
def count(a, k):
    # s=sin u, 2(1-s^2)+s=k → 2s^2 - s + (k-2) = 0
    ss = [s for s in sp.solve(2*sp.Symbol('s')**2 - sp.Symbol('s') + (k-2), sp.Symbol('s')) if s.is_real and -1 <= s <= 1]
    tot = set()
    for s in ss:
        base = [sp.asin(s), sp.pi - sp.asin(s)]
        for m in range(-1, a+1):
            for b in base:
                u = sp.nsimplify(b + 2*sp.pi*m)
                if 0 <= u <= 2*sp.pi*a: tot.add(sp.simplify(u))
    return len(tot)
pairs = [(a, k) for a in range(1, 31) for k in range(1, 4) if count(a, k) == 21]
print("q16 (a,k) =", pairs, " 합 =", sum(a+k for a, k in pairs)); assert sum(a+k for a, k in pairs) == 15
# q20: g(γ)=0((가)), g(α)=-1((나): 최솟값이 -1일 때만 근 1개), 2g(β)-g(α)=11((다))
gb = F(11 - 1, 2); print("q20 g(β) =", gb, " h(α)+h(γ) =", -1 + 2*gb); assert -1 + 2*gb == 9
# q27: 점화식 그대로 a_n 계산 후 합, (가)·(나) 식 확인
a = {1: F(2)}
for n in range(1, 21): a[n+1] = (2*n*(n+1)**2 + (n+1)*a[n]) / n
rr = sum(F(k) / a[k] for k in range(1, 21))
assert all(a[n] == n*n*(n+1) for n in a)
f20 = a[21]/21 - a[20]/20; g3 = a[3]/3
print("q27 r =", rr, " f(20) =", f20, " g(3) =", g3, " 값 =", f20*g3*rr); assert f20*g3*rr == 480
print("모두 일치")
