"""q6: 표본비율 0.2, 95% 신뢰구간 길이 0.098 → n — 정답 ③ 256."""
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
    p = F(1, 5)
    target = F(98, 1000)
    z = F(196, 100)
    # 길이 = 2·z·√(p(1−p)/n). 자연수 n 전수 탐색(1~10000), 제곱해서 정확 비교
    hits = [n for n in range(1, 10001) if (2 * z) ** 2 * p * (1 - p) / n == target**2]
    assert hits == [256], hits
    ans = hits[0]
    mark = check_choices(ans, [192, 224, 256, 288, 320], 3)
    return f"정답 {mark} {ans}"


run("q6", main)
