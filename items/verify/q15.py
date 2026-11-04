"""q15 검증: 수직선 위 점 P, x(t)=t^4+a t^3+b t^2+c t.
(가) v(1)=v(3)=0  (나) t>0에서 운동 방향이 바뀌는 시각은 오직 하나  (다) v(2)>0
묻는 값: 시각 t=4에서의 가속도. 정답 ① 28.
"""
import sys
from fractions import Fraction as F
import sympy as sp

t, a, b, c = sp.symbols("t a b c", real=True)
ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and cond


def poly_from_r(r):
    """(가)를 만족하는 모든 x(t): v의 최고차항 4, 근 1, 3 → 셋째 근 r(실수)."""
    v = 4 * (t - 1) * (t - 3) * (t - r)
    sol = sp.solve(sp.Poly(sp.diff(t**4 + a*t**3 + b*t**2 + c*t, t) - sp.expand(v), t).all_coeffs(), [a, b, c], dict=True)
    assert len(sol) == 1
    return (t**4 + a*t**3 + b*t**2 + c*t).subs(sol[0])


def direction_changes(x):
    """t>0에서 속도의 부호가 바뀌는 시각 목록(근 사이 표본점의 부호로 판정)."""
    v = sp.diff(x, t)
    roots = sorted({sp.nsimplify(r) for r in sp.real_roots(sp.Poly(v, t)) if r > 0})
    out = []
    for r0 in roots:
        eps = sp.Rational(1, 10**6)
        if sp.sign(v.subs(t, r0 - eps)) * sp.sign(v.subs(t, r0 + eps)) < 0:
            out.append(r0)
    return out


def accel4(x):
    return sp.diff(x, t, 2).subs(t, 4)


def conds(x, use=("가", "나", "다")):
    v = sp.diff(x, t)
    res = True
    if "가" in use:
        res &= v.subs(t, 1) == 0 and v.subs(t, 3) == 0
    if "나" in use:
        res &= len(direction_changes(x)) == 1
    if "다" in use:
        res &= v.subs(t, 2) > 0
    return bool(res)


# 후보 r: 정수·반정수·특수값을 넓게 훑는다 (r=1, r=3 포함)
R = sorted({F(k, 4) for k in range(-40, 41)} | {F(1), F(3), F(0)})
cands = [(r, poly_from_r(sp.Rational(r.numerator, r.denominator))) for r in R]

# (a)(b) 정답과 유일성: 세 조건 모두 → r=3 하나
sols = [(r, x) for r, x in cands if conds(x)]
check("세 조건 만족 후보는 r=3 하나", [r for r, _ in sols] == [F(3)])
xs = sols[0][1]
check("v(t)=4(t-1)(t-3)^2", sp.expand(sp.diff(xs, t) - 4*(t-1)*(t-3)**2) == 0)
ans = accel4(xs)
print("a, b, c =", sp.Poly(xs, t).all_coeffs()[1:4], " 가속도 a(4) =", ans)
check("정답 28", ans == 28)

# 기호 확인: (가)에서 v=4(t-1)(t-3)(t-r). (나) 만족 ⇔ r=1 또는 r=3 (r≤0: 두 번, 0<r≠1,3: 세 번 바뀜)
rs = sp.symbols("r", real=True)
check("(다): v(2)=4(r-2)>0 ⇔ r>2", sp.simplify((4*(t-1)*(t-3)*(t-rs)).subs(t, 2) - 4*(rs-2)) == 0)

# (c) 조건 필요성
def answers(use):
    return sorted({accel4(x) for r, x in cands if conds(x, use)})

no_ga_vals = set()
for p in range(-2, 6):           # (가) 제외: v의 두 근도 자유 → 몇 개만 표본
    for q in range(p, 6):
        for r in (0, 2, 4, 5, p):
            v = 4*(t-p)*(t-q)*(t-r)
            x = sp.integrate(v, (t, 0, t))
            if conds(x, ("나", "다")):
                no_ga_vals.add(accel4(x))
check("(가)를 빼면 답이 여럿", len(no_ga_vals) > 1)
A_na = answers(("가", "다"))
check("(나)를 빼면 답이 여럿 (r>2 전부)", len(A_na) > 1)
A_da = answers(("가", "나"))
print("(다) 제외 시 답 후보:", A_da)
check("(다)를 빼면 답 28, 60 두 개", A_da == [28, 60])

# (d) 선지·오답 경로
choices = [28, 36, 44, 52, 60]
check("선지 등간격 오름차순, 정답 ①", choices == sorted(choices) and len({choices[i+1]-choices[i] for i in range(4)}) == 1 and choices[0] == ans)
wrong_r1 = accel4(poly_from_r(1))           # (다) 무시/부호 착각: v=4(t-1)^2(t-3)
check("오답 r=1 경로 → 60 = ⑤", wrong_r1 == 60 and wrong_r1 in choices)
wrong_v = sp.diff(xs, t).subs(t, 4)        # 가속도 대신 속도
check("오답 속도 v(4)=12 → 선지 밖", wrong_v == 12 and wrong_v not in choices)
wrong_no4 = sp.diff(4*(t-1)*(t-3)**2/4, t).subs(t, 4)  # 최고차 계수 4 누락
check("오답 계수 4 누락 → 7 선지 밖", wrong_no4 == 7 and wrong_no4 not in choices)
wrong_pos = xs.subs(t, 4)                  # 위치를 답함
print("참고: x(4) =", wrong_pos)
check("정답 정수", ans.is_integer)

print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
