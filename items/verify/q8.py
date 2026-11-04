"""q8: ∫_{-2}^{2} (x³+3x²−4x+1) dx — 정답 ⑤ 20."""
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


def main():
    coef = [1, -4, 3, 1]  # 낮은 차수부터: 1 − 4x + 3x² + x³
    prim = lambda x: sum(F(c, i + 1) * x ** (i + 1) for i, c in enumerate(coef))
    ans = prim(F(2)) - prim(F(-2))
    assert ans.denominator == 1
    ans = int(ans)
    # 심프슨 공식(삼차 이하 다항식에서 정확)으로 교차 확인
    f = lambda x: x**3 + 3 * x**2 - 4 * x + 1
    simpson = F(4, 6) * (f(F(-2)) + 4 * f(F(0)) + f(F(2)))
    assert simpson == ans
    mark = check_choices(ans, [12, 14, 16, 18, 20], 5)
    return f"정답 {mark} {ans}"


run("q8", main)
