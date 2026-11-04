"""q6: 표본 크기 400, 표본비율 0.2, 95% 신뢰구간 길이 b−a — 정답 ③ 0.0784."""
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
    n = 400
    z = F(196, 100)
    # 길이 = 2·z·√(p(1−p)/n). √(p(1−p)/n) = √(16/40000) = 1/50 (정확한 유리수)
    var = p * (1 - p) / n
    s = F(1, 50)
    assert s * s == var, var
    ans = 2 * z * s
    assert ans == F(784, 10000), ans
    choices = [F(588, 10000), F(686, 10000), F(784, 10000), F(882, 10000), F(980, 10000)]
    mark = check_choices(ans, choices, 3)
    # 대표 오답: 2배 누락(0.0392), √ 누락(2·1.96·0.0004), 분산을 p̂/n으로(2·1.96·√(0.2/400)≈0.0877)
    assert z * s not in choices
    return f"정답 {mark} {float(ans)}"


run("q6", main)
