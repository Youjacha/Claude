#!/usr/bin/env python3
"""q28 검증 스크립트 (M1-25).  실행: python3 items/verify/q28.py   (필요: pip install sympy)

문항: 최고차항의 계수가 1인 삼차함수 f, g(t) = (|f(x)-f(t)| 가 미분가능하지 않은 x의 개수).
  (가) lim_{t->1} g(t) > g(1)
  (나) g(t)는 t=4에서 불연속
  f'(5)로 가능한 모든 값의 합 = 156

검증 방식
  (0) 기호 보조정리: f(x)-f(p∓d) = (x-(p∓d))^2 (x-(p±2d))  (sympy)
  (1) g(t)를 "풀이 공식(p±d, p±2d)"이 아니라 정의에서 직접 계산한다:
      F(x)=f(x)-f(t)=(x-t)Q(x), Q의 판별식·Q(t)로 단순근 개수를 Fraction으로 정확히 센다.
      (|F|는 F의 단순근에서만 미분 불가능: 중근·삼중근에서는 F'=0이라 미분가능 — 수치 좌우 미분계수로도 확인)
  (2) f(x)=x^3-3p x^2+3(p^2-e)x (상수항은 g에 영향 없음)를 격자 (p, e) 전수 탐색:
      p ∈ (1/6)Z∩[-12,12],  e ∈ {d^2 : d ∈ (1/6)Z, 0<d≤12} ∪ {0} ∪ {음수·비제곱 값}  (e<0 단조, e=0 정류 변곡, e>0 극값 2개)
  (3) 조건 하나씩 빼기, (4) 오답 경로 값, (5) 답 범위.
"""
import sys
from fractions import Fraction as Fr
from itertools import product

import sympy as sp

FAIL = []


def check(name, ok):
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        FAIL.append(name)


# ---------------------------------------------------------------- (0) 기호 보조정리
x, p, d, C = sp.symbols("x p d C", real=True)
f_sym = (x - p) ** 3 - 3 * d**2 * (x - p) + C
lem1 = sp.expand(f_sym - f_sym.subs(x, p - d) - (x - (p - d)) ** 2 * (x - (p + 2 * d)))
lem2 = sp.expand(f_sym - f_sym.subs(x, p + d) - (x - (p + d)) ** 2 * (x - (p - 2 * d)))
check("보조정리: f(x)-f(p-d)=(x-p+d)^2(x-p-2d), f(x)-f(p+d)=(x-p-d)^2(x-p+2d)", lem1 == 0 and lem2 == 0)


# ---------------------------------------------------------------- (1) g(t) 정의대로 계산
def g_exact(b, c, t):
    """f=x^3+bx^2+cx 일 때 F(x)=f(x)-f(t)의 서로 다른 단순 실근 개수 = |F|의 미분 불가능 점 개수."""
    # F(x) = (x-t)(x^2 + (t+b)x + (t^2+bt+c))
    B = t + b
    Cq = t * t + b * t + c
    disc = B * B - 4 * Cq
    Qt = t * t + B * t + Cq
    if disc < 0:
        return 1                      # t만 단순근
    if disc == 0:
        r = -B / 2
        return 0 if r == t else 1     # 삼중근 / (t 단순 + r 중근)
    # 서로 다른 두 근
    return 1 if Qt == 0 else 3        # t가 Q의 근이면 t 중근 + 나머지 단순근


def g_numeric(coeffs, t, h=1e-6):
    """수치 확인용: |f(x)-f(t)|의 좌우 미분계수가 다른 점 개수 (근 근처만 조사)."""
    import numpy as np
    b, c = coeffs
    ft = t**3 + b * t * t + c * t
    roots = np.roots([1, b, c, -ft])
    reals = sorted({round(r.real, 6) for r in roots if abs(r.imag) < 1e-7})
    cnt = 0
    for r in reals:
        F = lambda s: abs(s**3 + b * s * s + c * s - ft)
        left = (F(r) - F(r - h)) / h
        right = (F(r + h) - F(r)) / h
        if abs(left - right) > 1e-3:
            cnt += 1
    return cnt


EPS = Fr(1, 10**6)


def lim_both(b, c, a):
    return g_exact(b, c, a - EPS), g_exact(b, c, a + EPS)


def cond_ga(b, c):     # (가) lim_{t->1} g(t) 존재하고 g(1)보다 큼
    lo, hi = lim_both(b, c, Fr(1))
    return lo == hi and lo > g_exact(b, c, Fr(1))


def cond_na(b, c):     # (나) t=4에서 불연속
    lo, hi = lim_both(b, c, Fr(4))
    v = g_exact(b, c, Fr(4))
    return not (lo == hi == v)


def fprime(b, c, s):
    return 3 * s * s + 2 * b * s + c


# 수치 교차 확인: 정의 계산(g_exact)과 수치 좌우 미분계수 방식이 일치하는지 (임의 표본)
import random
random.seed(28)
agree = True
for _ in range(300):
    b = Fr(random.randint(-12, 12), random.choice([1, 2, 3]))
    c = Fr(random.randint(-30, 30), random.choice([1, 2, 3]))
    t = Fr(random.randint(-40, 40), 7)
    if g_exact(b, c, t) != g_numeric((float(b), float(c)), float(t)):
        agree = False
# 특수점(중근·삼중근) 확인
for (b, c, t) in [(Fr(-6), Fr(9), Fr(1)), (Fr(-6), Fr(9), Fr(3)), (Fr(-3), Fr(3), Fr(1)), (Fr(-6), Fr(9), Fr(4)), (Fr(-6), Fr(9), Fr(0))]:
    if g_exact(b, c, t) != g_numeric((float(b), float(c)), float(t)):
        agree = False
check("g(t) 정확 계산 = 수치 좌우 미분계수 판정 (표본 305개)", agree)


# ---------------------------------------------------------------- (2) 격자 전수 탐색
def grid():
    ps = [Fr(k, 6) for k in range(-72, 73)]
    es = sorted({Fr(k * k, 36) for k in range(1, 73)} | {Fr(0)} |
                {Fr(j, 12) for j in range(-24, 0)} | {Fr(j, 7) for j in (1, 2, 3, 5, 10, 20, 50)})
    for pp, e in product(ps, es):
        b = -3 * pp
        c = 3 * (pp * pp - e)
        yield pp, e, b, c


sols, only_na, only_ga, total = [], [], [], 0
for pp, e, b, c in grid():
    total += 1
    A, N = cond_ga(b, c), cond_na(b, c)
    if A and N:
        sols.append((pp, e, fprime(b, c, 5)))
    if N and not A:
        only_na.append((pp, e, fprime(b, c, 5)))
    if A and not N:
        only_ga.append((pp, e, fprime(b, c, 5)))

print(f"      격자 크기 {total}개 함수, (가)(나) 만족: {[(str(q), str(e), str(v)) for q, e, v in sols]}")
expected = {(Fr(5, 2), Fr(9, 4)): 12, (Fr(2), Fr(1)): 24, (Fr(-2), Fr(9)): 120}
check("해 집합 = {(p,d)=(5/2,3/2),(2,1),(-2,3)} (격자 전수, 3개뿐)",
      {(q, e): v for q, e, v in sols} == expected)
vals = sorted(v for _, _, v in sols)
answer = sum(vals)
print(f"      f'(5) 가능한 값: {vals} → 합 {answer}")
check("정답 156", answer == 156)

# 해마다 f'(x) 인수분해 확인 (sympy)
X = sp.Symbol("x")
for (q, e), v in expected.items():
    fp = sp.factor(3 * (X - sp.Rational(q.numerator, q.denominator)) ** 2 - 3 * sp.Rational(e.numerator, e.denominator))
    print(f"      p={q}, d^2={e}: f'(x) = {fp},  f'(5) = {v}")

# ---------------------------------------------------------------- (3) 조건 필요성
na_vals = {v for _, _, v in only_na} | set(vals)
ga_vals = {v for _, _, v in only_ga} | set(vals)
check(f"(가)를 빼면 f'(5) 후보가 늘어남 (격자에서 {len(na_vals)}개 값)", len(na_vals) > 3)
check(f"(나)를 빼면 f'(5) 후보가 늘어남 (격자에서 {len(ga_vals)}개 값, 정류 변곡 (x-1)^3 포함)",
      len(ga_vals) > 3 and any(e == 0 and q == 1 for q, e, _ in only_ga))
# 최고차항 계수 1을 빼면: af(x) (a>0)도 같은 g를 가지므로 f'(5)가 a배 → 정해지지 않음
b, c = -3 * Fr(2), 3 * (4 - 1)
# g는 f(x)-f(t)의 근 구조만 보므로 a·f(x) (a>0)도 같은 g를 가진다.
check("최고차항 계수 조건을 빼면 2f(x)도 (가)(나)를 만족 → f'(5)가 2배가 되어 답이 정해지지 않음",
      cond_ga(b, c) and cond_na(b, c) and 2 * fprime(b, c, 5) != fprime(b, c, 5))
# 극한 '>' 대신 '≠'로 쓰면: 양 끝점(p±2d=1)은 극한이 없어 여전히 제외 — 부등호는 정류 변곡·고립점 판정용
# (가)의 부등호 방향: lim < g(1) 인 경우는 없음을 확인
check("(가)에서 lim g(t) < g(t) 인 점은 존재하지 않음 (g의 고립점은 항상 아래로 떨어짐)",
      not any(lim_both(-3 * q, 3 * (q * q - e), Fr(1))[0] == lim_both(-3 * q, 3 * (q * q - e), Fr(1))[1]
              and lim_both(-3 * q, 3 * (q * q - e), Fr(1))[0] < g_exact(-3 * q, 3 * (q * q - e), Fr(1))
              for q, e, _, _ in list(grid())[::7]))

# ---------------------------------------------------------------- (4) 오답 경로
wrong = {
    "1, 4를 극대점·극소점으로 놓고 멈춤(경우 A1만)": 12,
    "1=p-d, 4=p+2d 한 경우만(가장 흔한 1:2 비율 풀이)": 24,
    "1이 극소점(p+d)인 경우 누락": 12 + 24,
    "4가 고립점(극소점)인 경우 누락": 24 + 120,
    "1=p-d, 4=p+2d 경우 누락": 12 + 120,
    "(나) 확인 없이 정류 변곡 f=(x-1)^3+C 포함": 156 + 48,
}
for k, v in wrong.items():
    print(f"      wrong: {k} → {v}")
check("오답 경로 값이 모두 정답 156과 다름", all(v != 156 for v in wrong.values()))

# ---------------------------------------------------------------- (5) 단답 범위
check("정답이 1~999 자연수", 1 <= answer <= 999)

print()
if FAIL:
    print(f"실패 {len(FAIL)}건: {FAIL}")
    sys.exit(1)
print("모두 통과: 정답 156")
