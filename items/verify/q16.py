#!/usr/bin/env python3
"""q16 검증 스크립트 (M1-17).

문항: 자연수 a, 실수 k에 대하여 0 <= x <= 2*pi 에서
      2cos^2(ax) + sin(ax) = k 의 서로 다른 실근의 개수가 21이 되도록 하는
      모든 순서쌍 (a, k)에 대하여 a+k 의 값의 합.  정답 ③ 35.

실행: python3 items/verify/q16.py   (pip install sympy)
방법: 해설의 개수식(4a+1, 3a, a ...)을 쓰지 않고,
  (1) t = sin(ax)에 대한 이차방정식의 근을 sympy로 구하고,
  (2) 각 근 t에 대해 sin(theta) = t 의 해를 sympy.solveset으로
      theta 구간 [0, 2*a*pi] (닫힌/반열린)에서 정확히 센다.
  k는 '개수가 바뀌는 임계값'과 임계값 사이 구간의 대표값을 모두 검사한다
  (구간 안에서는 t-근이 연속적으로 움직이며 0, ±1, 중근을 지나지 않으므로 개수 일정).
  추가로 x에 대한 수치 스캔(부호 변화 + 접점)으로 몇 개 경우를 교차 확인한다.
"""
import sys
from fractions import Fraction
import sympy as sp
import numpy as np

T = sp.Symbol('t', real=True)
TH = sp.Symbol('th', real=True)
fails = []

def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        fails.append(msg)

def count_roots(a, k, closed=True):
    """0<=x<=2pi (closed) 또는 0<=x<2pi 에서 2cos^2(ax)+sin(ax)=k 의 서로 다른 실근 수.
    a는 양의 유리수 허용(조건 필요성 실험용). theta=ax 로 두고, t-근마다
    sin(theta)=t 의 일반해 asin(t)+2n*pi, pi-asin(t)+2n*pi 를 정확한 sympy 값으로
    나열해 구간 [0, 2a*pi] 안의 것을 센다(theta와 x는 일대일).
    경계 비교는 60자리 정밀도 + 1e-40 허용오차(끝점에 정확히 걸리는 근 판정용)."""
    a = sp.nsimplify(a)
    k = sp.nsimplify(k)
    ts = sp.solveset(sp.Eq(2*(1 - T**2) + T, k), T, sp.Interval(-1, 1))
    hi = (2*a*sp.pi).evalf(60)
    eps = sp.Float('1e-40', 60)
    thetas = set()
    for t in ts:
        b = sp.asin(t).evalf(60)
        for n in range(-2, int(sp.ceiling(a)) + 2):
            for th in (b + 2*n*sp.pi.evalf(60), sp.pi.evalf(60) - b + 2*n*sp.pi.evalf(60)):
                if th < -eps:
                    continue
                if (th > hi + eps) if closed else (th > hi - eps):
                    continue
                thetas.add(round(float(th), 9))  # 서로 다른 근은 1e-3 이상 떨어짐
    return len(thetas)

# 임계 k: t=-1,0,1 을 지나는 값, 꼭짓점(중근) 값
crit = [sp.Integer(-1), sp.Integer(1), sp.Integer(2), sp.Rational(17, 8)]
mids = [sp.Integer(-2), sp.Integer(0), sp.Rational(3, 2), sp.Rational(33, 16), sp.Integer(3)]
KS = crit + mids

def solutions(N, closed=True, amax=30):
    out = []
    for a in range(1, amax + 1):
        for k in KS:
            if count_roots(a, k, closed) == N:
                out.append((a, k))
    return out

# 개수 >= a (근이 있는 모든 경우) 이므로 N=21 이면 a<=21 로 충분. 여유 있게 30까지.
sol = solutions(21)
print('(a,k) with 21 roots:', sol)
check(all(k in crit for _, k in sol), '해는 모두 임계값 k (구간 k는 개수 21 불가 → 순서쌍 유한)')
ans = sum(a + k for a, k in sol)
print('answer =', ans)
check(sorted(sol) == [(5, 2), (7, 1), (21, -1)], '순서쌍은 (5,2),(7,1),(21,-1) 셋뿐 (유일성)')
check(ans == 35, '정답 35')

# --- 수치 교차 확인 (x 직접 스캔) ---
def numeric_count(a, k, n=2_000_000):
    """x 직접 스캔: |f|의 국소 최솟값(끝점 포함)이 0에 가까운 점을 근으로 센다.
    교차근은 |f|min <= 기울기*h, 접근은 h^2 차수, 근이 아닌 극값은 1/8 이상 떨어짐."""
    x = np.linspace(0, 2*np.pi, n + 1)
    af = np.abs(2*np.cos(a*x)**2 + np.sin(a*x) - k)
    tol = 1e-3
    c = int(af[0] < tol and af[0] <= af[1]) + int(af[-1] < tol and af[-1] <= af[-2])
    loc = (af[1:-1] < af[:-2]) & (af[1:-1] <= af[2:]) & (af[1:-1] < tol)
    return c + int(np.sum(loc))
for a, k in [(5, 2), (7, 1), (21, -1), (4, sp.Rational(3, 2)), (3, 0), (6, sp.Rational(17, 8))]:
    ex = count_roots(a, k)
    nu = numeric_count(a, float(k))
    check(ex == nu, f'수치 교차 확인 a={a}, k={k}: exact {ex} = numeric {nu}')

# --- 조건 필요성 ---
# (1) 닫힌구간 -> 반열린구간 [0,2pi): (5,2) 가 빠지고 답이 28
sol_open = solutions(21, closed=False)
ans_open = sum(a + k for a, k in sol_open)
print('[0,2pi) 일 때:', sol_open, ans_open)
check(ans_open != 35 and ans_open == 28, '닫힌구간 조건 필요 (빼면 28 = 선지 ②)')

# (2) a 자연수 -> 양의 유리수: 21개가 되는 다른 순서쌍이 생김
extra = []
for num in range(1, 120):
    a = Fraction(num, 4)
    if a.denominator == 1:
        continue
    for k in KS:
        if count_roots(sp.Rational(a.numerator, a.denominator), k) == 21:
            extra.append((str(a), k))
print('a 비정수일 때 21개 예:', extra[:6], '... 총', len(extra))
check(len(extra) > 0, 'a 자연수 조건 필요 (빼면 순서쌍 추가)')

# (3) 개수 21(홀수) -> 짝수 20: 구간 k 에서 개수 20 → 순서쌍 무수히 많음
sol20 = solutions(20)
inf20 = [p for p in sol20 if p[1] in mids]
print('N=20 구간 대표 k 해:', inf20)
check(len(inf20) > 0, '개수 21(홀수) 조건 필요 (짝수면 k가 구간 → 순서쌍 무한)')

# --- 오답 경로 (wrong:) ---
def model_sum(model, N=21):
    return sum(a + k for k, f in model for a in range(1, 100) if f(a) == N)
wrong = {
    '끝점 누락(t=0을 2a개)': [(2, lambda a: 4*a), (1, lambda a: 3*a), (-1, lambda a: a)],
    't=1 근 누락(k=1에서 2a개)': [(2, lambda a: 4*a+1), (1, lambda a: 2*a), (-1, lambda a: a)],
    '접점 k=-1 누락': [(2, lambda a: 4*a+1), (1, lambda a: 3*a)],
    't=±1을 주기당 2개': [(2, lambda a: 4*a+1), (1, lambda a: 4*a), (-1, lambda a: 2*a)],
}
choices = [21, 28, 35, 42, 49]
check(choices[2] == ans, '정답이 ③')
check(all(choices[i+1] - choices[i] == 7 for i in range(4)), '선지 등간격 오름차순')
for name, m in wrong.items():
    v = model_sum(m)
    where = f'선지 {"①②③④⑤"[choices.index(v)]}' if v in choices else '선지 밖'
    print(f'wrong: {name} -> {v} ({where})')
    check(v != ans, f'오답 경로 "{name}" 값 {v} ≠ 정답')
check(model_sum(wrong['끝점 누락(t=0을 2a개)']) == 28, '대표 함정(끝점) 값 28이 선지 ②에 있음')

print()
if fails:
    print(f'FAILED {len(fails)}')
    sys.exit(1)
print('ALL PASS: q16 정답 ③ 35')
