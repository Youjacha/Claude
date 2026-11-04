"""q24: Σ_{k=1}^{10} a_k=24, Σ_{k=1}^{5} a_{2k−1}=7 일 때 Σ_{k=1}^{5}(3a_{2k}+k) — 정답 66."""
import sys
import random
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
    # 조건을 만족하는 임의의 수열 여러 개로 값이 항상 같음(불변)을 확인
    vals = set()
    rng = random.Random(1)
    for _ in range(500):
        a = [rng.randint(-20, 20) for _ in range(10)]  # a[0]=a_1, …
        odd = sum(a[0::2]); even = sum(a[1::2])
        a[0] += 7 - odd          # 홀수 번째 항의 합을 7로
        a[1] += 17 - even        # 전체 합을 24로
        assert sum(a) == 24 and sum(a[0::2]) == 7
        vals.add(sum(3 * a[2 * k - 1] + k for k in range(1, 6)))
    assert len(vals) == 1, vals
    ans = vals.pop()
    check_short(ans, 1, 200)
    return f"정답 {ans}"


run("q24", main)
