#!/usr/bin/env python3
"""q16 검증 스크립트 (M1-17).

문항: 두 자연수 a, k에 대하여 0 <= x <= 2*pi 에서
      2cos^2(ax) + sin(ax) = k 의 서로 다른 실근의 개수가 21이 되도록 하는
      모든 순서쌍 (a, k)에 대하여 a+k 의 값의 합.  정답 ③ 15.
      (M1-8 변경: k를 실수 → 자연수로 좁힘. 실수 k일 때의 결과는 조건 필요성에서 비교.)

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
KS_REAL = crit + mids
# 자연수 k: 2cos^2+sin 의 최댓값은 17/8 이므로 k>=3 이면 근이 없다. 3은 그 확인용.
KS = [sp.Integer(1), sp.Integer(2), sp.Integer(3)]

def solutions(N, closed=True, amax=30, ks=None):
    ks = KS if ks is None else ks
    out = []
    for a in range(1, amax + 1):
        for k in ks:
            if count_roots(a, k, closed) == N:
                out.append((a, k))
    return out

# 개수 >= a (근이 있는 모든 경우) 이므로 N=21 이면 a<=21 로 충분. 여유 있게 30까지.
sol = solutions(21)
print('(a,k) with 21 roots:', sol)
check(all(count_roots(a, 3) == 0 for a in (1, 5, 7)), 'k>=3 이면 근 없음 (k 후보는 1, 2뿐)')
ans = sum(a + k for a, k in sol)
print('answer =', ans)
check(sorted(sol) == [(5, 2), (7, 1)], '순서쌍은 (5,2),(7,1) 둘뿐 (유일성)')
check(ans == 15, '정답 15')

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
# (1) 닫힌구간 -> 반열린구간 [0,2pi): (5,2) 가 빠지고 답이 8
sol_open = solutions(21, closed=False)
ans_open = sum(a + k for a, k in sol_open)
print('[0,2pi) 일 때:', sol_open, ans_open)
check(ans_open != 15 and ans_open == 8, '닫힌구간 조건 필요 (빼면 8)')

# (2) a 자연수 -> 양의 유리수: 21개가 되는 다른 순서쌍이 생김
extra = []
for num in range(1, 30 * 40):
    a = Fraction(num, 40)   # 분모 40 격자: 2, 4, 5, 8 등의 분모를 함께 훑음
    if a.denominator == 1:
        continue
    for k in KS[:2]:
        if count_roots(sp.Rational(a.numerator, a.denominator), k) == 21:
            extra.append((str(a), k))
print('a 비정수일 때 21개 예:', extra[:6], '... 총', len(extra))
check(len(extra) > 0, 'a 자연수 조건 필요 (빼면 순서쌍 추가)')

# (3) k 자연수 -> 실수: (21,-1) 이 추가되어 답 35 (검수 전 문항)
sol_real = solutions(21, ks=KS_REAL)
ans_real = sum(a + k for a, k in sol_real)
print('k 실수일 때:', sol_real, ans_real)
check(sorted(sol_real) == [(5, 2), (7, 1), (21, -1)] and ans_real == 35, 'k 자연수 조건 필요 (실수면 35)')
# (4) 개수 21 -> 20: 자연수 k 에서는 해 없음 (개수 3a, 4a+1 꼴)
check(solutions(20) == [], '개수 20이면 해 없음 (21이 3a·4a+1 꼴을 모두 만족하는 값)')

# --- 오답 경로 (wrong:) ---
def model_sum(model, N=21):
    return sum(a + k for k, f in model for a in range(1, 100) if f(a) == N)
wrong = {
    '끝점 누락(t=0을 2a개)': [(2, lambda a: 4*a), (1, lambda a: 3*a)],
    't=1 근 누락(k=1에서 2a개)': [(2, lambda a: 4*a+1), (1, lambda a: 2*a)],
    't=±1을 주기당 2개': [(2, lambda a: 4*a+1), (1, lambda a: 4*a)],
    'k=2에서 t=1/2 근 누락(2a+1개)': [(2, lambda a: 2*a+1), (1, lambda a: 3*a)],
}
choices = [7, 11, 15, 19, 23]
check(choices[2] == ans, '정답이 ③')
check(all(choices[i+1] - choices[i] == 4 for i in range(4)), '선지 등간격 오름차순')
for name, m in wrong.items():
    v = model_sum(m)
    where = f'선지 {"①②③④⑤"[choices.index(v)]}' if v in choices else '선지 밖'
    print(f'wrong: {name} -> {v} ({where})')
    check(v != ans, f'오답 경로 "{name}" 값 {v} ≠ 정답')
check(model_sum(wrong['t=1 근 누락(k=1에서 2a개)']) == 7, '대표 함정(접점 t=1 누락) 값 7이 선지 ①에 있음')

print()
if fails:
    print(f'FAILED {len(fails)}')
    sys.exit(1)
print('ALL PASS: q16 정답 ③ 15')
