"""q27 검증: 수열의 합과 일반항 빈칸 추론 (정답 261).

조건: a_1 = 3, n >= 2 인 모든 자연수 n 에 대하여 S_n = (4/5) a_n + n^2/5 + 4.
묻는 값: (나)=p=a_2, (다)=q=sum_{k=1}^{12} a_k + 3 sum_{k=1}^{5} a_{2k+1},
(가)=f(n) 에 대하여 p*q/f(7).
풀이 식(점화식)을 쓰지 않고, S_n 식을 n=2,3,... 순서로 직접 풀어 a_n 을 만든다.
"""
import sys
from fractions import Fraction as F
import sympy as sp

ok = True
def check(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and cond

N = 30
ALPHA = F(4, 5)
def P(n, c=4):
    return F(n * n, 5) + c

def build(a1, c=4, n_max=N):
    """S_n = ALPHA a_n + P(n) (n>=2) 를 a_n 에 대한 일차방정식으로 직접 풀어 수열 생성."""
    a = {1: F(a1)}
    S = F(a1)
    for n in range(2, n_max + 1):
        # S_{n-1} + a_n = ALPHA a_n + P(n)  ->  a_n = (P(n) - S_{n-1}) / (1 - ALPHA)
        a[n] = (P(n, c) - S) / (1 - ALPHA)
        S += a[n]
    return a

def answer_parts(a):
    p = a[2]
    q = sum(a[k] for k in range(1, 13)) + 3 * sum(a[2 * k + 1] for k in range(1, 6))
    return p, q

# (가): sympy 로 독립 계산. a_{n+1} = S_{n+1}-S_n = ALPHA(a_{n+1}-a_n) + [P(n+1)-P(n)]
n = sp.symbols('n')
Pn = n**2 / 5 + 4
f_expr = sp.simplify(Pn.subs(n, n + 1) - Pn)
check("(가) f(n) = (2n+1)/5", sp.simplify(f_expr - (2 * n + 1) / 5) == 0)
f7 = F(str(f_expr.subs(n, 7)))

a = build(3)
# (a) 정답
p, q = answer_parts(a)
ans = p * q / f7
print(f"f(7)={f7}, p=a_2={p}, q={q}, answer={ans}")
check("(나) p = 9", p == 9)
check("(다) q = 87", q == 87)
check("정답 261", ans == 261)
check("단답 1~999 자연수", ans.denominator == 1 and 1 <= ans <= 999)

# 생성한 수열이 n=2..N 에서 S_n 식을 만족, n=1 에서는 불성립(첫째항 예외)
S = 0
good = True
for k in range(1, N + 1):
    S += a[k]
    if k >= 2:
        good = good and (S == ALPHA * a[k] + P(k))
check("S_n 식 n=2..30 성립", good)
check("S_1 식 불성립(n=1 예외)", a[1] != ALPHA * a[1] + P(1))
# ㉠ 4a_n + a_{n+1} = 2n+1 은 n>=2 에서만 성립
check("㉠ n>=2 성립", all(4 * a[k] + a[k + 1] == 2 * k + 1 for k in range(2, N)))
check("㉠ n=1 불성립", 4 * a[1] + a[2] != 3)

# (b) 유일성: a_n 은 n>=2 에서 일차방정식(계수 1-ALPHA=1/5 != 0)의 유일 해 -> 수열 유일.
#     기호로도 확인: a_2 를 미지수로 두고 n=2 식을 풀면 해 1개.
x = sp.symbols('x')
sol = sp.solve(sp.Eq(3 + x, sp.Rational(4, 5) * x + sp.Rational(4, 5) + 4), x)
check("유일성: a_2 해 1개 = 9", sol == [9])

# (c) 조건 필요성
# c1) a_1=3 을 빼면 a_1 에 따라 답이 달라짐
vals = set()
for a1 in range(-5, 10):
    pp, qq = answer_parts(build(a1))
    vals.add(pp * qq / f7)
check("a_1 조건 제거 -> 답 여러 개", len(vals) > 1)
# c2) 'n>=2' 를 'n>=1' 로 바꾸면 a_1 = 3 과 모순 (해 없음); a_1 자유로 두면 a_1 이 강제되나 다른 값
a1_forced = sp.solve(sp.Eq(x, sp.Rational(4, 5) * x + sp.Rational(1, 5) + 4), x)
check("n>=1 이면 a_1=3 과 모순", a1_forced != [3])
# c3) S_n 식을 n>=3 에서만 주면 a_2 가 자유 -> 답 여러 개
def build_free_a2(a2):
    a = {1: F(3), 2: F(a2)}
    S = a[1] + a[2]
    for k in range(3, N + 1):
        a[k] = (P(k) - S) / (1 - ALPHA)
        S += a[k]
    return a
vals = {(lambda pq: pq[0] * pq[1] / f7)(answer_parts(build_free_a2(t))) for t in range(0, 15)}
check("n=2 식 제거 -> 답 여러 개", len(vals) > 1)
# c4) 상수항 4 를 바꾸면 답이 달라짐(상수항이 a_2 를 정함)
check("상수항 변경 -> 답 변화", answer_parts(build(3, c=5)) != (p, q))

# (d) 대표 오답 경로 (단답이므로 선지 대신 결과 값 점검)
wrong = {
    "㉠을 n=1 에 적용 (a_2=-9)": F(-9) * (3 - 9 + 75) / f7,
    "(다)에서 a_1 누락": p * (q - 3) / f7,
    "f(n) 을 5×(가)=2n+1 로": p * q / 15,
    "f(n) 을 P(n)=n^2/5 로": p * q / F(49, 5),
}
for k, v in wrong.items():
    print(f"  오답 경로 {k}: {v} ({float(v):.3f})")
check("오답 값이 정답과 다름", all(v != ans for v in wrong.values()))

print("ALL PASS" if ok else "SOME FAILED")
sys.exit(0 if ok else 1)
