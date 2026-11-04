"""q25: f(x)=2x³+ax²+12x+b 가 x=2에서 극솟값 10 → 극댓값 — 정답 11."""
import sys
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
    found = []
    for a in range(-100, 101):
        for b in range(-200, 201):
            f = lambda x: 2 * x**3 + a * x**2 + 12 * x + b
            fp = lambda x: 6 * x**2 + 2 * a * x + 12
            if fp(2) != 0 or f(2) != 10:
                continue
            # x=2가 극소: f′ 가 − → + 로 바뀜
            if not (fp(2 - 1e-6) < 0 < fp(2 + 1e-6)):
                continue
            found.append((a, b))
    assert found == [(-9, 6)], found
    a, b = found[0]
    f = lambda x: 2 * x**3 + a * x**2 + 12 * x + b
    fp = lambda x: 6 * x**2 + 2 * a * x + 12
    # 다른 임계점(극대) 찾기: 정수 근 탐색
    crit = [x for x in range(-50, 51) if fp(x) == 0]
    assert crit == [1, 2], crit
    assert fp(1 - 1e-6) > 0 > fp(1 + 1e-6)
    ans = f(1)
    check_short(ans, 1, 200)
    return f"정답 {ans} (a={a}, b={b})"


run("q25", main)
