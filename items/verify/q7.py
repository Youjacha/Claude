"""q7: π<θ<3π/2, tanθ=2√2 일 때 cosθ — 정답 ② −1/3."""
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
    # 제3사분면에서 tan θ = 2√2 인 θ 를 수치로 구함
    theta = math.pi + math.atan(2 * math.sqrt(2))
    assert math.pi < theta < 1.5 * math.pi
    ans = math.cos(theta)
    s2 = math.sqrt(2)
    # 오름차순: sin 혼동, 정답, 부호 실수, 1/tan 착각, sin 혼동+부호 실수
    choices = [-2 * s2 / 3, -1 / 3, 1 / 3, s2 / 4, 2 * s2 / 3]
    mark = check_choices(ans, choices, 2, tol=1e-12)
    assert all(abs(c) <= 1 for c in choices), "선지가 [-1,1] 밖"
    wrong = {"sin 혼동": math.sin(theta), "부호 실수": -ans, "1/tan": 1 / math.tan(theta), "혼동+부호": -math.sin(theta)}
    for k, v in wrong.items():
        assert any(abs(v - c) < 1e-12 for c in choices) and abs(v - ans) > 1e-9, k
    # 기호 확인: cos²θ = 1/9, cosθ<0 → −1/3
    assert abs(ans**2 - 1 / 9) < 1e-12 and ans < 0
    return f"정답 {mark} −1/3 ({ans:.6f})"


run("q7", main)
