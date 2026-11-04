"""q27 검증: 수열의 귀납적 정의 + 치환 + 부분분수 빈칸 추론 (정답 480). M1-8 재설계.

조건: a_1 = 2, 모든 자연수 n 에 대하여 n·a_{n+1} - (n+1)·a_n = 2n(n+1)^2.
빈칸: (가) f(n) — a_{n+1}/(n+1) = a_n/n + f(n),
      (나) g(n) — a_n/n = g(n),
      (다) r     — sum_{k=1}^{20} k/a_k.
묻는 값: f(20) × g(3) × r.

풀이 식(치환·망원합)을 쓰지 않고, 점화식으로 a_1..a_N 을 Fraction 으로 직접 만든 뒤
(가)(나)는 생성한 수열에서 다항식을 맞춰(보간) 얻고, (다)는 직접 합한다.
"""
import sys
from fractions import Fraction as F
import sympy as sp

ok = True


def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and cond


N = 40


def build(a1=2, rhs=lambda n: 2 * n * (n + 1) ** 2, n_max=N):
    """n a_{n+1} = (n+1) a_n + rhs(n) 를 a_{n+1} 에 대해 풀어 생성(계수 n != 0 이라 유일)."""
    a = {1: F(a1)}
    for n in range(1, n_max):
        a[n + 1] = (F(n + 1) * a[n] + rhs(n)) / n
    return a


n = sp.symbols('n')


def fit(points, deg):
    """정수점 (n, 값) 들로 다항식 보간 후 나머지 점에서 일치하는지 확인."""
    poly = sp.interpolate(points[: deg + 1], n)
    good = all(sp.nsimplify(poly.subs(n, x)) == sp.nsimplify(y) for x, y in points)
    return sp.expand(poly), good


def parts(a):
    diffs = [(k, a[k + 1] / (k + 1) - a[k] / k) for k in range(1, N)]
    b = [(k, a[k] / k) for k in range(1, N + 1)]
    f_poly, f_ok = fit([(x, sp.Rational(y.numerator, y.denominator)) for x, y in diffs], 3)
    g_poly, g_ok = fit([(x, sp.Rational(y.numerator, y.denominator)) for x, y in b], 4)
    r = sum(F(k) / a[k] for k in range(1, 21))
    return f_poly, f_ok, g_poly, g_ok, r


def value(f_poly, g_poly, r):
    return F(str(f_poly.subs(n, 20))) * F(str(g_poly.subs(n, 3))) * r


a = build()
f_poly, f_ok, g_poly, g_ok, r = parts(a)
print(f"(가) f(n) = {f_poly}, (나) g(n) = {sp.factor(g_poly)}, (다) r = {r}")
check("(가) f(n) = 2n+2 (n=1..39 모두 일치)", f_ok and sp.expand(f_poly - (2 * n + 2)) == 0)
check("(나) g(n) = n(n+1) (n=1..40 모두 일치)", g_ok and sp.expand(g_poly - n * (n + 1)) == 0)
check("일반항 a_n = n^2(n+1)", all(a[k] == k * k * (k + 1) for k in range(1, N + 1)))
check("(다) r = 20/21", r == F(20, 21))
ans = value(f_poly, g_poly, r)
print(f"f(20)={f_poly.subs(n, 20)}, g(3)={g_poly.subs(n, 3)}, r={r} -> answer={ans}")
check("정답 480", ans == 480)
check("단답 1~999 자연수", ans.denominator == 1 and 1 <= ans <= 999)

# 유일성: a_{n+1} 의 계수 n 이 0 이 아니므로 a_1 이 정해지면 수열이 하나로 정해진다(build 가 그 구성).
# 기호로도 확인: a_{n+1} 을 미지수로 둔 일차방정식의 해가 하나.
x = sp.symbols('x')
check("유일성: n=1..10 에서 a_{n+1} 의 해가 하나",
      all(len(sp.solve(sp.Eq(k * x - (k + 1) * sp.Rational(a[k].numerator, a[k].denominator), 2 * k * (k + 1) ** 2), x)) == 1
          for k in range(1, 11)))

# 조건 필요성
# c1) a_1 = 2 를 바꾸면 (나)·(다)가 바뀌고 답이 달라짐(부분분수가 깔끔히 소거되지 않음)
vals = {}
for a1 in (1, 3, 4, 6):
    fp, _, gp, _, rr = parts(build(a1))
    vals[a1] = value(fp, gp, rr)
print("  a_1 변경 시 답:", {k: str(v) for k, v in vals.items()})
check("a_1 조건 필요 (바꾸면 답이 달라짐)", all(v != ans for v in vals.values()))
# c2) 오른쪽 식 2n(n+1)^2 을 바꾸면 답이 달라짐
fp, _, gp, _, rr = parts(build(rhs=lambda k: 2 * k * (k + 1)))
v2 = value(fp, gp, rr)
check("오른쪽 식 변경 -> 답 변화", v2 != ans)
# c3) '모든 자연수 n' 을 'n>=2' 로 바꾸면 a_2 가 자유 -> 답 여러 개
def build_free_a2(a2):
    a = {1: F(2), 2: F(a2)}
    for k in range(2, N):
        a[k + 1] = (F(k + 1) * a[k] + 2 * k * (k + 1) ** 2) / k
    return a
free = set()
for a2 in (6, 10, 12, 20):
    aa = build_free_a2(a2)
    free.add(sum(F(k) / aa[k] for k in range(1, 21)))
check("n=1 에서의 성립 필요 (빼면 r 여러 개)", len(free) > 1)

# 대표 오답 경로
f20, g3 = 42, 12
wrong = {
    "(나)에서 Σ를 n까지(g=(n+1)(n+2)), r 도 그에 맞춰 5/11": F(f20) * 20 * F(5, 11),
    "(나)에서 Σ를 n까지, r 은 20/21 그대로": F(f20) * 20 * F(20, 21),
    "(다) 망원합 끝항 실수 1-1/20": F(f20) * g3 * F(19, 20),
    "(가)를 2(n+1)^2/n 등으로(나눗셈 실수) f(20)=2*21^2/20": F(2 * 21 * 21, 20) * g3 * F(20, 21),
}
for k, v in wrong.items():
    print(f"  오답 경로 {k}: {v} ({'정수' if v.denominator == 1 else '비정수'})")
check("오답 값이 정답과 다름", all(v != ans for v in wrong.values()))

print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
