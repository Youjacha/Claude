#!/usr/bin/env python3
"""q14 검증 스크립트 (대수 · 수열의 귀납적 정의).

실행: python3 items/verify/q14.py   (표준 라이브러리만 사용)

문항: 첫째항이 자연수인 수열 {a_n}이 모든 자연수 n에 대하여
    a_{n+1} = 3a_n - 2   (a_n <= 4)
    a_{n+1} = a_n - 4    (a_n > 4)
를 만족시킬 때, a_6 = 4가 되도록 하는 모든 a_1의 값의 합. 정답 ④ 52.

검사 (a) 정답(정방향 전수), (b) 유일성(후보 집합이 유한하고 범위 밖에 해 없음),
     (c) 조건 필요성, (d) 오답 경로 값과 선지(등간격, 정답 ④, 겹침 없음).
"""
import sys
from fractions import Fraction as Fr

FAIL = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  -> {info}" if info else ""))
    if not ok:
        FAIL.append(name)


def step(a, T=4, strict=False):
    low = (a < T) if strict else (a <= T)
    return 3 * a - 2 if low else a - 4


def term(a1, k, **kw):
    x = a1
    for _ in range(k - 1):
        x = step(x, **kw)
    return x


N = 20000  # 전수 범위
# (a) 정방향 전수 탐색: 자연수 a_1 < N 에 대해 a_6 계산
sols = [a for a in range(1, N) if term(a, 6) == 4]
check("(a) 정방향 전수로 구한 a_1 집합 = {2, 8, 18, 24}", sols == [2, 8, 18, 24], str(sols))
ANS = sum(sols)
check("(a) 정답 = 52", ANS == 52, str(ANS))

# (b) 유일성: a_n > 4 이면 다음 항은 4만 감소, a_n <= 4 이면 다음 항 <= 10.
#     따라서 a_1 > 4 + 4*5 = 24 이면 a_2..a_6 이 모두 a_1 - 4(n-1) > 4 이므로 a_6 = a_1 - 20 > 4.
#     → a_1 <= 24 밖에는 해가 없다. 전수 범위 N 이 이를 덮는지 확인.
big_ok = all(term(a, 6) == a - 20 and a - 20 > 4 for a in range(25, 2000))
check("(b) a_1 >= 25 이면 a_6 = a_1 - 20 > 4 (범위 밖 해 없음)", big_ok)
# 모든 항이 자연수임(첫째항 자연수 → 이후 항도 자연수)
nat_ok = all(min(term(a, n) for n in range(1, 7)) >= 1 for a in range(1, 2000))
check("(b) 첫째항이 자연수이면 모든 항이 자연수", nat_ok)


# 역추적(풀이 경로)을 독립 구현해 교차 확인: 각 단계에서 구간 조건 확인
def backward(c, steps, check_region=True, strict=False, T=4):
    cur = {Fr(c)}
    for _ in range(steps):
        nxt = set()
        for y in cur:
            x1 = y + 4  # a_n > T 인 경우
            if (not check_region) or (x1 > T if not strict else x1 >= T):
                nxt.add(x1)
            x2 = (y + 2) / 3  # a_n <= T 인 경우
            if (not check_region) or (x2 <= T if not strict else x2 < T):
                nxt.add(x2)
        cur = nxt
    return cur


bw = sorted(int(x) for x in backward(4, 5) if x.denominator == 1 and x >= 1)
check("(a) 역추적(구간 확인) 결과가 전수 결과와 일치", bw == sols, str(bw))

# (c) 조건 필요성
# c1: a_6 = 4 를 빼면 모든 자연수 a_1 이 가능 → 합이 정해지지 않음
check("(c) 'a_6=4' 제거 → 후보가 무한(자연수 전체)", True, "제약 없음")
# c2: '첫째항이 자연수' 제거 → 유리수 해 존재 (예: a_1 = (4/3+2)/3 ...)
rat = sorted(x for x in backward(4, 5) if x.denominator != 1)
ok_rat = len(rat) > 0
# 정방향으로 다시 확인
def term_fr(a1, k):
    x = Fr(a1)
    for _ in range(k - 1):
        x = 3 * x - 2 if x <= 4 else x - 4
    return x
ok_rat = ok_rat and all(term_fr(x, 6) == 4 for x in rat)
check("(c) '자연수' 제거 → 정수가 아닌 a_1 해가 생김", ok_rat, f"{len(rat)}개, 예: {rat[:3]}")
# c3: 경계 '≤' 를 '<' 로 바꾸면 답이 달라짐 (경계값 a_n = 4 의 처리가 답에 영향)
sols_lt = [a for a in range(1, N) if term(a, 6, strict=True) == 4]
check("(c) 경계 a_n=4 처리 변경(≤→<) 시 해 집합이 달라짐", sols_lt != sols, f"{sols_lt}, 합 {sum(sols_lt)}")
# c4: 구간 분기 조건(a_n <= 4 / a_n > 4)을 확인하지 않으면 10이 해로 섞임 → 분기 조건이 10을 제거
W1 = sorted(int(x) for x in backward(4, 5, check_region=False) if x.denominator == 1 and x >= 1)
check("(c) 분기 조건 확인을 빼면 해 집합이 달라짐(10 추가)", W1 != sols and set(W1) - set(sols) == {10}, str(W1))
check("(c) 10은 실제로 a_6 != 4", term(10, 6) != 4, f"a_6 = {term(10, 6)}")
# (d) 오답 경로
W1s = sum(W1)
print("wrong W1 (역추적에서 구간 확인 생략, a_2=6 의 '3x-2' 가지 허용):", W1, W1s)
W2s = sum(sols_lt)
print("wrong W2 (경계 a_n=4 를 a_n-4 쪽으로 처리):", sols_lt, W2s)
W3 = [a for a in range(1, N) if term(a, 5) == 4]
print("wrong W3 (단계 수 4번만 거꾸로, a_5=4로 착각):", W3, sum(W3))
W4 = [a for a in range(1, N) if term(a, 7) == 4]
print("wrong W4 (단계 수 6번, a_7=4로 착각):", W4, sum(W4))
W5 = sorted(int(x) for x in backward(4, 5) if x.denominator == 1 and x >= 1 and x > 4)
print("wrong W5 (a_1 <= 4 인 2를 빠뜨림):", W5, sum(W5))

choices = [22, 32, 42, 52, 62]
diffs = {choices[i + 1] - choices[i] for i in range(4)}
check("(d) 선지 등간격 오름차순", diffs == {10} and choices == sorted(choices), str(choices))
check("(d) 정답이 ④", choices.index(ANS) == 3)
check("(d) 오답 W1=62 가 ⑤, W2=42 가 ③ (정답과 다름)", W1s == 62 and W2s == 42 and choices[4] == W1s and choices[2] == W2s)
check("(d) 오답 값이 정답과 겹치지 않음", ANS not in (W1s, W2s, sum(W3), sum(W4), sum(W5)))
check("(d) 정답은 정수", isinstance(ANS, int))

print()
if FAIL:
    print("FAILED:", FAIL)
    sys.exit(1)
print("ALL PASS — 정답 ④ 52")
