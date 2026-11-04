"""q10: [1,13]에서 f(x)=log₂(x+a)+b 의 최댓값 5, 최솟값 3 → a+b — 정답 ④ 4."""
import sys
import math
# --- 공용 검사 함수(문항 파일마다 동일) ---
CIRCLED = "①②③④⑤"


def check_choices(answer, choices, planned, key=lambda v: v, tol=None):
    """선지가 정렬 규칙대로이고 정답과 같은 선지가 정확히 하나이며 그 번호가 계획과 같은지 확인한다.

    key: 정렬 기준(음수는 절댓값 순이므로 key=abs).
    tol: 실수 비교 허용 오차(None이면 정확히 비교).
    """
    ks = [key(c) for c in choices]
    assert ks == sorted(ks) and len(set(ks)) == 5, f"선지 정렬/중복 오류: {choices}"
    eq = (lambda a, b: a == b) if tol is None else (lambda a, b: abs(a - b) < tol)
    hits = [i for i, c in enumerate(choices) if eq(c, answer)]
    assert len(hits) == 1, f"정답과 같은 선지 수 {len(hits)}개: answer={answer}, choices={choices}"
    idx = hits[0] + 1
    assert idx == planned, f"정답 번호 {idx} ≠ 계획 {planned}"
    return CIRCLED[idx - 1]


def check_short(answer, lo, hi):
    assert isinstance(answer, int) and lo <= answer <= hi, f"단답 범위 오류: {answer} not in [{lo}, {hi}]"


def run(name, fn):
    try:
        msg = fn()
    except AssertionError as e:
        print(f"{name}: 실패 — {e}")
        sys.exit(1)
    print(f"{name}: 통과 — {msg}")
# --- 끝 ---


def main():
    # a 를 촘촘하게 훑어 최댓값−최솟값 = 2 인 a 찾기(이분법; 차이는 a 에 대해 감소)
    diff = lambda a: math.log2(13 + a) - math.log2(1 + a)
    lo, hi = -1 + 1e-12, 1e6
    assert diff(lo) > 2 > diff(hi)
    for _ in range(200):
        mid = (lo + hi) / 2
        (lo, hi) = (mid, hi) if diff(mid) > 2 else (lo, mid)
    a = round(lo)
    assert abs(lo - a) < 1e-9
    b = 5 - math.log2(13 + a)
    assert abs(b - round(b)) < 1e-12
    b = round(b)
    # 원래 조건 재확인(구간 전체 샘플링)
    xs = [1 + 12 * i / 1000 for i in range(1001)]
    ys = [math.log2(x + a) + b for x in xs]
    assert abs(max(ys) - 5) < 1e-12 and abs(min(ys) - 3) < 1e-12
    ans = a + b
    mark = check_choices(ans, [1, 2, 3, 4, 5], 4)
    return f"정답 {mark} {ans} (a={a}, b={b})"


run("q10", main)
