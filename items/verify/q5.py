"""q5: f(x)=(x²+2)(2x³−x+1) 일 때 f′(1) — 정답 ④ 19."""
import sys
from fractions import Fraction as F
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


def polymul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r


def main():
    # 전개한 다항식(계수: 낮은 차수부터)을 직접 미분
    p = polymul([2, 0, 1], [1, -1, 0, 2])
    dp = [i * c for i, c in enumerate(p)][1:]
    ans = sum(dp)  # x=1 대입
    # 차분 몫으로 교차 확인
    f = lambda x: (x * x + 2) * (2 * x**3 - x + 1)
    h = F(1, 10**8)
    assert abs((f(1 + h) - f(1 - h)) / (2 * h) - ans) < F(1, 10**6)
    mark = check_choices(ans, [16, 17, 18, 19, 20], 4)
    return f"정답 {mark} {ans}"


run("q5", main)
