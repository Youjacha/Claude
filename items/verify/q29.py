"""q29 검증 — 두 주머니 공 교환 시행, 조건부확률 (정답 262).

공에 번호를 붙여(같은 색이라도 서로 다른 공) 3번의 시행을 모두 열거한다.
한 번의 시행은 A의 공 3개 중 1개, B의 공 4개 중 1개를 고르는 12가지가 같은 확률이다.
확률은 Fraction으로 계산한다.

확인 항목
 (a) 정답: P(서로 다른 색 교환이 있었음 | 3회 후 A의 흰 공 1개) = 113/149, p+q = 262
 (b) 유일성: 기약분수 표현이 하나, 262는 1~999 자연수
 (c) 조건 필요성: 조건을 빼거나 바꾸면 답이 달라짐
 (d) 대표 오답 경로 값이 정답과 다름
"""
import sys
from fractions import Fraction as F
from math import gcd

FAIL = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    if not ok:
        FAIL.append(name)


def enumerate_runs(A0, B0, n):
    """A0, B0: 색 리스트('W' 흰, 'K' 검). 각 실행을 (A 흰 공 수 경로, 시행별 교환 색 쌍) 으로 돌려준다."""
    A0 = [(c, ('A', i)) for i, c in enumerate(A0)]
    B0 = [(c, ('B', i)) for i, c in enumerate(B0)]
    runs = []

    def rec(A, B, path, swaps, k):
        if k == n:
            runs.append((tuple(path), tuple(swaps)))
            return
        for i in range(len(A)):
            for j in range(len(B)):
                A2, B2 = A[:], B[:]
                A2[i], B2[j] = B[j], A[i]
                w = sum(1 for c, _ in A2 if c == 'W')
                rec(A2, B2, path + [w], swaps + [(A[i][0], B[j][0])], k + 1)

    rec(A0, B0, [sum(1 for c, _ in A0 if c == 'W')], [], 0)
    return runs


A_INIT = ['W', 'K', 'K']        # 주머니 A: 흰 공 1, 검은 공 2
B_INIT = ['W', 'W', 'K', 'K']   # 주머니 B: 흰 공 2, 검은 공 2
N = 3

runs = enumerate_runs(A_INIT, B_INIT, N)
TOTAL = len(runs)
check("전체 경우의 수 12^3", TOTAL == 12 ** 3, str(TOTAL))


def diff_swap(r):
    return any(a != b for a, b in r[1])


def prob(event, given=lambda r: True):
    den = [r for r in runs if given(r)]
    num = [r for r in den if event(r)]
    return F(len(num), len(den))


cond = lambda r: r[0][-1] == 1          # 3회 후 A의 흰 공 1개(처음과 같음)

# (a) 정답
ans = prob(diff_swap, cond)
p, q = ans.denominator, ans.numerator
check("(a) 조건부확률 = 113/149", ans == F(113, 149), str(ans))
check("(a) p+q = 262", p + q == 262, str(p + q))

# 독립 재계산: 색만 보는 상태(A의 흰 공 수) 전이 행렬로 다시 계산 (개수 /12)
def trans(w):
    bw = 3 - w                      # B의 흰 공 수 (전체 흰 공 3개)
    down = w * (4 - bw)             # A 흰 ↔ B 검
    up = (3 - w) * bw               # A 검 ↔ B 흰
    stay = 12 - down - up
    return {w - 1: down, w + 1: up, w: stay}

def chain(start, n):
    paths = {(start,): 1}
    for _ in range(n):
        nxt = {}
        for pa, c in paths.items():
            for s, m in trans(pa[-1]).items():
                if m:
                    nxt[pa + (s,)] = nxt.get(pa + (s,), 0) + c * m
        paths = nxt
    return paths

ch = chain(1, 3)
den2 = sum(c for pa, c in ch.items() if pa[-1] == 1)
num2 = sum(c for pa, c in ch.items() if pa[-1] == 1 and len(set(pa)) > 1)
check("(a) 상태 전이 재계산 894, 678", (den2, num2) == (894, 678), f"{num2}/{den2}")
check("(a) 두 계산 일치", F(num2, den2) == ans)

# (b) 유일성·범위
check("(b) 기약분수", gcd(p, q) == 1)
check("(b) 1~999 자연수", 1 <= p + q <= 999)
# 조건을 만족하면 3번 중 상태가 바뀐 횟수는 0 또는 2 (홀짝)
changes = {sum(1 for x, y in zip(r[0], r[0][1:]) if x != y) for r in runs if cond(r)}
check("(b) 조건 하에서 상태 변화 횟수 ∈ {0,2}", changes == {0, 2}, str(sorted(changes)))

# (c) 조건 필요성
no_cond = prob(diff_swap)
check("(c) 조건(3회 후 흰 공 1개) 제거 시 답이 달라짐", no_cond != ans, f"{no_cond}")
for e in (0, 2, 3):
    v = prob(diff_swap, lambda r, e=e: r[0][-1] == e)
    check(f"(c) 조건을 '흰 공 {e}개'로 바꾸면 답이 달라짐", v != ans, f"{v}")
# '서로 다른 색 교환'을 '같은 색 교환'으로 바꾸면 다른 값
same = prob(lambda r: any(a == b for a, b in r[1]), cond)
check("(c) 묻는 사건을 '같은 색 교환이 있었음'으로 바꾸면 달라짐", same != ans, str(same))
# 초기 구성(B의 흰 공 2개)이 필요: B를 흰1·검3으로 바꾸면 값이 달라짐
runs_b = enumerate_runs(A_INIT, ['W', 'K', 'K', 'K'], N)
den_b = [r for r in runs_b if r[0][-1] == 1]
v_b = F(sum(1 for r in den_b if diff_swap(r)), len(den_b))
check("(c) B 구성을 바꾸면 달라짐", v_b != ans, str(v_b))

# (d) 대표 오답 경로
wrong = {
    "조건부 아님 678/1728": F(678, 1728),
    "가운데 머묾을 상태1의 6으로 셈 756/972": F(756, 972),
    "(1,3)번째 변화 경우 누락 504/720": F(504, 720),
    "1→0→1 경로 누락 408/624": F(408, 624),
}
for k, v in wrong.items():
    s = v.numerator + v.denominator
    check(f"(d) 오답 [{k}] = {v} → {s} ≠ 262", s != 262 and v != ans)
joint = prob(lambda r: cond(r) and diff_swap(r))
check("(d) 조건부 아님(교집합 확률) 값 재확인", joint == F(678, 1728), str(joint))

print()
print(f"정답: q/p = {ans}, p+q = {p + q}")
if FAIL:
    print("실패:", FAIL)
    sys.exit(1)
print("모두 통과")
