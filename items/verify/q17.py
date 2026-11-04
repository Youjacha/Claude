"""q17 검증: 미적분Ⅰ · 두 곡선 사이의 넓이 (넓이 차, 보조 영역 더하고 빼기)

문항: 곡선 C: y = f(x) = x^3+2x^2+x (x>=0), 점 P(1,4)에서의 접선 l, l의 x절편 R.
1<m<4, 직선 y=mx 와 C의 원점이 아닌 교점 S, l과의 교점 Q.
A = 곡선과 선분 OS로 둘러싸인 부분, B = 곡선과 선분 SQ, QP로 둘러싸인 부분.
A - B = 1/12 일 때 m = ?   정답 ⑤ 8/3

검증은 풀이의 지름길(보조 영역)을 쓰지 않고, 교점 S를 직접 구해 A, B를 정적분으로 계산한다.
"""
import sys
from sympy import (symbols, Rational, sqrt, integrate, diff, solve, simplify,
                   nsimplify, Poly, real_roots, S as SS)

x, m, t = symbols('x m t', real=True)
f = x**3 + 2*x**2 + x
D = Rational(1, 12)
CHOICES = [Rational(8, 7), Rational(4, 3), Rational(8, 5), Rational(2), Rational(8, 3)]
ANSWER_NO = 5
fails = []


def check(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        fails.append(msg)


# ---- 기본 도형 ----
P = (1, f.subs(x, 1))
slope = diff(f, x).subs(x, 1)
tan = slope*(x - 1) + P[1]
R = solve(tan, x)[0]
check(P == (1, 4) and slope == 8 and R == Rational(1, 2), f"P={P}, 접선 y={tan}, R=({R},0)")
# 곡선이 [0,1]에서 접선보다 위(아래로 볼록) → 영역 B가 잘 정의됨
check(all((f - tan).subs(x, Rational(k, 100)) >= 0 for k in range(0, 101)), "0<=x<=1에서 곡선이 접선 위에 있음")


def geometry(mv):
    """m 값에 대해 S, Q의 x좌표와 A, B를 교점 S를 직접 써서 계산(지름길 미사용)."""
    sx = [r for r in solve(f - mv*x, x) if r.is_real and r > 0]
    assert len(sx) == 1, sx
    s = simplify(sx[0])
    q = solve(mv*x - tan, x)[0]
    A = integrate(mv*x - f, (x, 0, s))
    # B: x in [s,q] 에서 곡선-직선 y=mx, x in [q,1] 에서 곡선-접선
    B = integrate(f - mv*x, (x, s, q)) + integrate(f - tan, (x, q, 1))
    return s, q, simplify(A), simplify(B)


def config_ok(mv):
    s, q, A, B = geometry(mv)
    return bool(0 < s < q < 1 and R < q)


# ---- (a) 정답: 교점 S를 그대로 써서 A-B=1/12 을 풀기 (t = sqrt(m)) ----
# S의 x좌표는 (x+1)^2=m 에서 sqrt(m)-1. m = t^2 로 두고 t에 대한 방정식으로 푼다.
s_t = t - 1
q_t = 4/(8 - t**2)
A_t = integrate(t**2*x - f, (x, 0, s_t))
B_t = integrate(f - t**2*x, (x, s_t, q_t)) + integrate(f - tan, (x, q_t, 1))
eq = simplify((A_t - B_t - D)*(8 - t**2)**3)
num = Poly(simplify(eq.as_numer_denom()[0]), t)
roots_t = [r for r in real_roots(num) if 1 < r < 2]
roots_m = sorted(set(nsimplify(r**2) for r in roots_t))
print("  A-B=1/12, 1<m<4 의 해 m:", roots_m)
check(roots_m == [Rational(8, 3)], "정답 m = 8/3 (교점 S를 직접 쓴 독립 계산)")
s, q, A, B = geometry(Rational(8, 3))
check(simplify(A - B - D) == 0, f"m=8/3: S_x={s}, Q_x={q}, A={A}, B={B}, A-B={simplify(A-B)}")
check(config_ok(Rational(8, 3)), "m=8/3 에서 0<S_x<Q_x<1, Q가 선분 RP 위")
check(not s.is_rational, "S의 x좌표가 무리수 (직접 계산 경로는 무거움 → 지름길 관문 의미 있음)")

# ---- (b) 유일성: 1<m<4 에서 A-B 는 m에 대해 순증가 → 해 하나 ----
grid = [1 + Rational(k, 60) for k in range(1, 180)]
vals = []
for mv in grid:
    s_, q_, A_, B_ = geometry(mv)
    vals.append(float(A_ - B_))
check(all(b > a for a, b in zip(vals, vals[1:])), "1<m<4 격자 179점에서 A-B 순증가 (해 유일)")
check(all(config_ok(mv) for mv in grid[::10]), "1<m<4 전 범위에서 도형 배치 유지(S, Q 위치)")

# 지름길 공식과 일치 확인: A-B = (삼각형 OQR) - (곡선·접선·x축 영역) = m/(8-m) - 5/12
for mv in [Rational(3, 2), Rational(2), Rational(5, 2), Rational(7, 2)]:
    s_, q_, A_, B_ = geometry(mv)
    check(simplify(A_ - B_ - (mv/(8 - mv) - Rational(5, 12))) == 0, f"m={mv}: 직접 계산 A-B = m/(8-m)-5/12")

# ---- (c) 조건 필요성 ----
# 1) A-B=1/12 를 빼면: 1<m<4 의 모든 m 이 배치를 만족 → m 결정 불가
check(len(set(round(v, 9) for v in vals)) > 100, "조건 A-B=1/12 없으면 m 무수히 많음 (A-B 값이 m마다 다름)")
# 2) x>=0 제한을 빼면: 직선 y=mx 와 곡선의 원점 아닌 교점이 2개 → S 가 하나로 정해지지 않음
all_s = [r for r in solve(f - Rational(8, 3)*x, x) if r != 0]
check(len(all_s) == 2 and any(r < 0 for r in all_s), f"x>=0 없으면 원점 아닌 교점 2개 {all_s} → S 모호")
# 3) 1<m<4 를 빼면: m<=1 이면 S 없음, m>=4 이면 S가 P를 지나치거나 같아 B 정의 불가
check(not [r for r in solve(f - x, x) if r.is_real and r > 0], "m=1 이면 x>0 교점 S 없음 (A 정의 불가)")
s4 = [r for r in solve(f - 4*x, x) if r.is_real and r > 0][0]
q4 = solve(4*x - tan, x)[0]
check(s4 == 1 and q4 == 1, "m=4 이면 S=Q=P (B 넓이 0, 영역 붕괴) → 범위 조건은 배치 정의용(풀이 열쇠)")
# 공식 m/(8-m)-5/12 = 1/12 의 해는 범위 밖에 다른 해가 없지만, 범위 조건은 도형 정의를 위해 필요
sol_all = solve(m/(8 - m) - Rational(5, 12) - D, m)
check(sol_all == [Rational(8, 3)], "지름길 방정식 해도 8/3 하나")

# ---- (d) 선지: 크기 순, 정답 ⑤, 오답 경로 값 ----
check(CHOICES == sorted(CHOICES) and len(set(CHOICES)) == 5, "선지 오름차순·중복 없음")
check(CHOICES[ANSWER_NO - 1] == Rational(8, 3), "정답 번호 ⑤ (설계표 §4)")
check(all(c.q != 1 for c in [CHOICES[ANSWER_NO-1]]), "정답 기약분수 8/3")
W = Rational(5, 12)
paths = {
    "부호 바꿈(B-A=1/12로 세움)": solve(m/(8 - m) - (W - D), m),
    "삼각형 OQR 밑변을 OH=1로(또는 1/2 누락)": solve(2*m/(8 - m) - (W + D), m),
    "밑변 OH=1 + 부호 바꿈": solve(2*m/(8 - m) - (W - D), m),
    "[선지 밖] ∫0^1(mx-f)=1/12 오적용(접선 무시)": solve(integrate(m*x - f, (x, 0, 1)) - D, m),
    "[선지 밖] 접선 아래 삼각형을 빼지 않음(W=17/12)": solve(m/(8 - m) - (integrate(f, (x, 0, 1)) + D), m),
}
for k, v in paths.items():
    print(f"  오답 경로 {k}: m = {v}")
check(paths["부호 바꿈(B-A=1/12로 세움)"] == [Rational(2)], "④ 2 = 부호 바꿈 경로")
check(paths["삼각형 OQR 밑변을 OH=1로(또는 1/2 누락)"] == [Rational(8, 5)], "③ 8/5 = 삼각형 밑변/1/2 착오 경로")
check(paths["밑변 OH=1 + 부호 바꿈"] == [Rational(8, 7)], "① 8/7 = 두 착오 겹친 경로")
check(all(v[0] not in CHOICES or v[0] == Rational(8, 3) for k, v in paths.items() if k.startswith('[선지 밖]'))
      and paths["[선지 밖] ∫0^1(mx-f)=1/12 오적용(접선 무시)"] == [Rational(3)],
      "선지 밖 오답 3, 24/5 → 재검토 유도")
check(Rational(4, 3) == Rational(8, 6), "② 4/3 = 8/6 (선지 8/7, 8/6, 8/5, 8/4, 8/3 등분자 배열의 간격 선지)")
check(all(1 < c < 4 and config_ok(c) for c in CHOICES), "모든 선지 값이 1<m<4 배치 성립 → 범위로 소거 불가")

print()
if fails:
    print(f"FAILED {len(fails)}"); sys.exit(1)
print("ALL PASS: q17 정답 ⑤ 8/3")
