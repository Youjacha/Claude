#!/usr/bin/env python3
"""q21 검증: 문자 A 3개, B 3개, C 4개 일렬 배열.
(가) A끼리 이웃하지 않는다.  (나) 이웃한 두 문자가 A와 B인 곳이 정확히 4곳.
표준 라이브러리만 사용. 실패 시 종료 코드 1."""
import sys
from itertools import combinations, permutations
from math import comb

NA, NB, NC, M = 3, 3, 4, 4
OPTIONS = [140, 145, 150, 155, 160]   # ①~⑤ (오름차순)
ANSWER_POS = 3                        # ③
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    if not ok:
        fails.append(name)


def all_words():
    n = NA + NB + NC
    for As in combinations(range(n), NA):
        rest = [i for i in range(n) if i not in As]
        for Bs in combinations(rest, NB):
            w = ['C'] * n
            for i in As:
                w[i] = 'A'
            for i in Bs:
                w[i] = 'B'
            yield ''.join(w)


def ab_count(w):
    return sum(1 for i in range(len(w) - 1) if {w[i], w[i + 1]} == {'A', 'B'})


def no_aa(w):
    return 'AA' not in w


# ---------- (a) 전수 탐색 ----------
W = list(all_words())
check("전체 배열 수 10!/(3!3!4!) = 4200", len(W) == 4200, str(len(W)))
brute = sum(1 for w in W if no_aa(w) and ab_count(w) == M)
check("전수 탐색 정답 150", brute == 150, str(brute))


# ---------- 구조식(풀이와 독립적인 매개변수형 공식) ----------
def structural(aa_forced=True, bb_forced=False, at_least=False, choose=True, rest_forced=True,
               only_T=None):
    """C를 지운 A/B 열(뼈대)마다: 교대 칸 T개 중 j개를 비우고(나머지 교대 칸은 C≥1),
    AA 칸(aa_forced면 C≥1), BB 칸·양 끝은 자유. 오답 경로는 옵션으로 흉내 낸다."""
    total = 0
    for w in sorted(set(''.join(p) for p in permutations('A' * NA + 'B' * NB))):
        T = sum(1 for i in range(len(w) - 1) if w[i] != w[i + 1])
        aa = sum(1 for i in range(len(w) - 1) if w[i] == w[i + 1] == 'A')
        bb = sum(1 for i in range(len(w) - 1) if w[i] == w[i + 1] == 'B')
        if only_T is not None and T not in only_T:
            continue
        for j in ([M] if not at_least else range(M, T + 1)):
            if T < j:
                continue
            slots = len(w) + 1 - j
            forced = (T - j if rest_forced else 0) + (aa if aa_forced else 0) + (bb if bb_forced else 0)
            rem = NC - forced
            if rem < 0:
                continue
            total += (comb(T, j) if choose else 1) * comb(rem + slots - 1, slots - 1)
    return total


struct = structural()
check("구조식 = 전수 탐색", struct == brute, f"{struct} vs {brute}")
cases = {"T=5 (ABABAB, BABABA)": structural(only_T={5}),
         "T=4 전체": structural(only_T={4})}
check("경우별 값 100 / 50(=30+20)", cases["T=5 (ABABAB, BABABA)"] == 100 and cases["T=4 전체"] == 50,
      str(cases))

# ---------- (b) 해의 유일성: 경우의 수 문항이므로 답은 하나. 같은 문자 비구별 확인 ----------
sols = {w for w in W if no_aa(w) and ab_count(w) == M}
check("조건을 만족하는 서로 다른 문자열 150개(중복 없음)", len(sols) == 150 == brute)

# ---------- (c) 조건 필요성 ----------
drop_ga = sum(1 for w in W if ab_count(w) == M)
drop_na = sum(1 for w in W if no_aa(w))
check("(가)를 빼면 답이 바뀜", drop_ga != brute, f"(가) 제거 → {drop_ga}")
check("(나)를 빼면 답이 바뀜", drop_na != brute, f"(나) 제거 → {drop_na}")
check("'같은 문자 구별 안 함' 단서를 빼면 답이 바뀜", brute * 6 * 6 * 24 != brute, f"→ {brute*6*6*24}")

# ---------- (d) 오답 경로와 선지 ----------
wrong = {
    "BB 칸도 C 필수로 착각": structural(bb_forced=True),
    "(가) 무시, AA 칸 자유": structural(aa_forced=False),
    "'정확히 4'를 '4 이상'으로": structural(at_least=True),
    "T=5에서 비울 칸 고르기(×5) 누락": structural(choose=False),
    "T=4 뼈대 누락": structural(only_T={5}),
    "T=5의 남은 교대 칸을 자유로 둠": structural(rest_forced=False),
}
for k, v in wrong.items():
    print(f"     오답 경로 {k}: {v}")
check("오답 값이 정답과 다름", all(v != brute for v in wrong.values()))
check("선지 오름차순 등간격", all(OPTIONS[i + 1] - OPTIONS[i] == 5 for i in range(4)))
check("정답이 ③", OPTIONS[ANSWER_POS - 1] == brute)
in_opts = {k: v for k, v in wrong.items() if v in OPTIONS}
check("대표 오답 140(①), 160(⑤)이 선지에 있음",
      wrong["BB 칸도 C 필수로 착각"] == 140 and wrong["(가) 무시, AA 칸 자유"] == 160 and len(in_opts) >= 2,
      str(in_opts))
check("나머지 오답(70, 100, 200)은 선지 밖",
      all(v not in OPTIONS for k, v in wrong.items() if k not in in_opts))

print()
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print(f"모두 통과: 정답 ③ {brute}")
