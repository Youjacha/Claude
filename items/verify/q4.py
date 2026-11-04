"""q4: 등차수열 a₅=7, a₂+a₆=8 일 때 a₁₀ — 정답 ① 22."""
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
    # 첫째항 a, 공차 d 의 연립방정식을 정수 격자에서 전수 탐색 + 일반해 확인
    sols = [(a, d) for a in range(-50, 51) for d in range(-50, 51)
            if a + 4 * d == 7 and (a + d) + (a + 5 * d) == 8]
    assert sols == [(-5, 3)], sols
    # 계수 행렬식 ≠ 0 이므로 실수 해도 하나뿐
    assert 1 * 6 - 4 * 2 != 0
    a, d = sols[0]
    ans = a + 9 * d
    mark = check_choices(ans, [22, 24, 26, 28, 30], 1)
    return f"정답 {mark} {ans}"


run("q4", main)
