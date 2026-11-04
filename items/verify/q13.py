"""q13: X~N(m,σ²), P(X≤12)=P(X≥20), P(X≥20)=0.1587 → P(14≤X≤22) — 정답 ⑤ 0.6247."""
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

TABLE = {0.5: 0.1915, 1.0: 0.3413, 1.5: 0.4332, 2.0: 0.4772}  # 발문에 주는 표


def phi0(z):  # P(0 ≤ Z ≤ z), 실제 정규분포
    return 0.5 * math.erf(z / math.sqrt(2))


def main():
    # 표 값이 실제 정규분포 값과 맞는지
    for z, v in TABLE.items():
        assert abs(phi0(z) - v) < 5e-5, (z, v)
    m = (12 + 20) / 2  # 대칭
    # P(X≥20)=0.5−P(0≤Z≤(20−m)/σ)=0.1587 → 표에서 z=1
    zs = [z for z, v in TABLE.items() if abs(0.5 - v - 0.1587) < 1e-9]
    assert zs == [1.0]
    sigma = (20 - m) / zs[0]
    z1, z2 = (14 - m) / sigma, (22 - m) / sigma
    ans = round(TABLE[abs(z1)] + TABLE[z2], 4)
    assert abs(ans - (phi0(z2) - phi0(z1))) < 1e-3
    choices = [0.3830, 0.4332, 0.4772, 0.5328, 0.6247]
    mark = check_choices(ans, choices, 5, tol=1e-9)
    return f"정답 {mark} {ans} (m={m:g}, σ={sigma:g})"


run("q13", main)
