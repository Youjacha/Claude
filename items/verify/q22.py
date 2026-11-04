"""q22: log₃(x+1)+log₃(x−5)=3 의 해 — 정답 8."""
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
    # 진수 조건 x>5 에서 정수·유리 후보 전수 + 단조성으로 유일성
    sols = [x for x in range(6, 1000) if (x + 1) * (x - 5) == 27]
    assert sols == [8], sols
    # 좌변은 x>5 에서 증가하므로 실수 해도 하나
    g = lambda x: math.log(x + 1, 3) + math.log(x - 5, 3)
    assert all(g(5 + i / 100) < g(5 + (i + 1) / 100) for i in range(1, 2000))
    assert abs(g(8) - 3) < 1e-12
    ans = sols[0]
    check_short(ans, 1, 99)
    return f"정답 {ans}"


run("q22", main)
