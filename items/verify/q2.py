"""q2: f(x)=x³−2x²+4x, lim_{h→0} {f(1+2h)−f(1)}/h — 정답 ⑤ 6."""
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


def f(x):
    return x**3 - 2 * x**2 + 4 * x


def main():
    # 극한식 자체를 h → 0으로 보내며 수치 계산(유리수 정확 계산)
    vals = [(f(1 + 2 * F(1, 10**k)) - f(1)) / F(1, 10**k) for k in (4, 6, 8)]
    approx = vals[-1]
    ans = round(approx)
    assert abs(approx - ans) < F(1, 10**6)
    assert ans == 2 * (3 * 1 - 4 * 1 + 4)  # 2f'(1)
    mark = check_choices(ans, [2, 3, 4, 5, 6], 5)
    return f"정답 {mark} {ans}"


run("q2", main)
