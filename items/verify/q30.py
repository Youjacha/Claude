"""q30 검증 (표준 라이브러리만 사용).

f(x) = 3^((x-a+8)/4) - b,   g(x) = log_9 (x+b)^8 + a - 8   (x != -b)
(가) y=f(x), y=g(x)가 만나는 모든 점의 x좌표의 집합이 {a, b, c}
(나) c < 0
정답: a^2+b^2 = q/p (서로소)  ->  p+q

풀이 식을 옮기지 않고, (a, b)에 대한 연립방정식 f(a)=g(a), f(b)=g(b)를
여러 출발점에서 2차원 뉴턴법으로 수치 풀이한 뒤, 각 후보마다 교점 전체를
격자 탐색 + 이분법으로 다시 구해 조건을 판정한다.
"""
import math
import sys
from fractions import Fraction

LN3 = math.log(3.0)


def f(x, a, b):
    return 3.0 ** ((x - a + 8.0) / 4.0) - b


def g(x, a, b):
    # log_9 (x+b)^8 = 8*ln|x+b| / ln 9
    return 8.0 * math.log(abs(x + b)) / math.log(9.0) + a - 8.0


def h(x, a, b):
    return f(x, a, b) - g(x, a, b)


def intersections(a, b, lo=-400.0, hi=400.0, n=160000):
    """y=f(x)와 y=g(x)의 모든 교점의 x좌표 (점근선 x=-b 양쪽을 따로 탐색)."""
    roots = []
    for (L, R) in ((lo, -b - 1e-12), (-b + 1e-12, hi)):
        if L >= R:
            continue
        # 점근선 근처는 로그 간격으로 촘촘히
        xs = []
        for i in range(n + 1):
            t = i / n
            xs.append(L + (R - L) * t)
        near = -b - 1e-12 if R == -b - 1e-12 else -b + 1e-12
        sgn = -1 if R == -b - 1e-12 else 1
        for k in range(1, 60):
            xs.append(near + sgn * 10.0 ** (1 - k / 4.0))
        xs = sorted(x for x in xs if L <= x <= R)
        prev = None
        for x in xs:
            try:
                v = h(x, a, b)
            except (ValueError, OverflowError):
                prev = None
                continue
            if v == 0.0:
                roots.append(x)
            elif prev is not None and prev[1] * v < 0:
                l, r = prev[0], x
                for _ in range(200):
                    m = (l + r) / 2
                    if h(l, a, b) * h(m, a, b) <= 0:
                        r = m
                    else:
                        l = m
                roots.append((l + r) / 2)
            prev = (x, v)
    out = []
    for r in sorted(roots):
        if not out or abs(r - out[-1]) > 1e-7:
            out.append(r)
    return out


def newton2(a, b, it=200):
    for _ in range(it):
        try:
            F1, F2 = h(a, a, b), h(b, a, b)
            e = 1e-7
            J11 = (h(a + e, a + e, b) - h(a - e, a - e, b)) / (2 * e)
            J12 = (h(a, a, b + e) - h(a, a, b - e)) / (2 * e)
            J21 = (h(b, a + e, b) - h(b, a - e, b)) / (2 * e)
            J22 = (h(b + e, a, b + e) - h(b - e, a, b - e)) / (2 * e)
        except (ValueError, OverflowError, ZeroDivisionError):
            return None
        det = J11 * J22 - J12 * J21
        if abs(det) < 1e-14:
            return None
        da = (F1 * J22 - F2 * J12) / det
        db = (J11 * F2 - J21 * F1) / det
        lam = 1.0
        if abs(da) > 5 or abs(db) > 5:
            lam = 5 / max(abs(da), abs(db))
        a, b = a - lam * da, b - lam * db
        if not (abs(a) < 1e4 and abs(b) < 1e4):
            return None
        if abs(da) + abs(db) < 1e-13:
            break
    try:
        if abs(h(a, a, b)) < 1e-9 and abs(h(b, a, b)) < 1e-9:
            return (a, b)
    except (ValueError, OverflowError):
        return None
    return None


def candidates():
    """a, b가 모두 교점의 x좌표인 (a, b) 전부 (a=b 포함)."""
    sols = []
    starts = [x / 2.0 for x in range(-40, 41)]
    for a0 in starts:
        for b0 in starts:
            if abs(a0 + b0) < 1e-9 or abs(b0) < 1e-9:
                continue
            s = newton2(a0 + 0.013, b0 - 0.007)
            if s and not any(abs(s[0] - t[0]) < 1e-6 and abs(s[1] - t[1]) < 1e-6 for t in sols):
                sols.append(s)
    # a = b 인 경우는 1변수 방정식 h(t, t, t) = 0
    for t0 in starts:
        t = t0 + 0.011
        for _ in range(200):
            try:
                v = h(t, t, t)
                d = (h(t + 1e-7, t + 1e-7, t + 1e-7) - h(t - 1e-7, t - 1e-7, t - 1e-7)) / 2e-7
                t -= v / d
            except (ValueError, OverflowError, ZeroDivisionError):
                t = None
                break
        if t is not None and abs(h(t, t, t)) < 1e-9 and not any(abs(t - u[0]) < 1e-6 and abs(t - u[1]) < 1e-6 for u in sols):
            sols.append((t, t))
    return sols


def check(a, b, use_set=True, use_neg=True):
    S = intersections(a, b)
    def has(v):
        return any(abs(v - s) < 1e-6 for s in S)
    if not (has(a) and has(b)):
        return False
    rest = [s for s in S if abs(s - a) > 1e-6 and abs(s - b) > 1e-6]
    if use_set:
        # 집합 {a,b,c}와 같다: 교점이 a, b와 c 하나뿐 (원소 수는 {a,b,c}의 크기)
        if len(rest) != 1 or len(S) != len({round(a, 6), round(b, 6), round(rest[0], 6)}):
            return False
        cs = rest
    else:
        # 완화: a, b, c가 교점의 x좌표이기만 하면 됨 (c는 아무 교점)
        cs = S
    if use_neg:
        return any(c < 0 for c in cs)
    return True


fails = 0
def ok(cond, msg):
    global fails
    print(("[통과] " if cond else "[실패] ") + msg)
    if not cond:
        fails += 1


cands = candidates()
print("a, b 가 모두 교점 x좌표인 후보:", [(round(a, 6), round(b, 6)) for a, b in cands])

# (a)(b) 정답과 유일성
good = [(a, b) for a, b in cands if check(a, b)]
ok(len(good) == 1, f"조건 (가)(나)를 만족하는 (a,b)는 하나: {[(round(a,6), round(b,6)) for a,b in good]}")
a, b = good[0]
ok(abs(a - 8.5) < 1e-9 and abs(b - 0.5) < 1e-9, "a = 17/2, b = 1/2")
S = intersections(a, b)
c = [s for s in S if abs(s - a) > 1e-6 and abs(s - b) > 1e-6][0]
print(f"   교점 x좌표: {[round(s, 6) for s in S]}  (c ≈ {c:.6f})")
# 정확한 값 확인: f(17/2) = 3^2 - 1/2, f(1/2) = 3^0 - 1/2, 그리고 오른쪽 가지는 f의 역함수
A, B = Fraction(17, 2), Fraction(1, 2)
ok(Fraction(3) ** 2 - B == A and Fraction(3) ** 0 - B == B, "정확값: f(17/2)=17/2, f(1/2)=1/2 (3의 지수 (a-a+8)/4=2, (b-a+8)/4=0)")
val = A * A + B * B
p, q = val.denominator, val.numerator
ans = p + q
ok(val == Fraction(145, 2), f"a^2+b^2 = {val}")
ok(1 <= ans <= 999, f"정답 p+q = {ans} (1~999 자연수)")
ok(ans == 147, "정답 147")
# 역함수 관계 수치 확인: x > -b에서 g(f(x)) = x
ok(all(abs(g(f(x, a, b), a, b) - x) < 1e-9 for x in [-3, -1, 0, 2, 5, 9]), "x>-b 가지에서 g = f^{-1} (g(f(x)) = x)")

# (c) 조건 필요성
noneg = [(a_, b_) for a_, b_ in cands if check(a_, b_, use_neg=False)]
ok(len(noneg) >= 2, f"(나) c<0 제거 → 해 {len(noneg)}개: {[(round(x,6), round(y,6)) for x,y in noneg]}")
noset = [(a_, b_) for a_, b_ in cands if check(a_, b_, use_set=False)]
ok(any(abs(x - y) < 1e-9 for x, y in noset) and len(noset) >= 2,
   f"(가)의 '집합이 정확히 {{a,b,c}}' 완화 → a=b 후보 생김: {[(round(x,6), round(y,6)) for x,y in noset]}")
# 'a가 교점' 제거: 임의의 a에 대해 b가 교점 x좌표이고 c<0인 b가 존재 (연속 해족)
fam_a = 0
for a_ in [2.0, 3.0, 5.0, 7.0, 11.0]:
    for b0 in [0.3, 1.0, 2.0, 4.0]:
        bb = b0
        try:
            for _ in range(100):
                v = h(bb, a_, bb)
                d = (h(bb + 1e-7, a_, bb + 1e-7) - h(bb - 1e-7, a_, bb - 1e-7)) / 2e-7
                bb -= v / d
            if abs(h(bb, a_, bb)) < 1e-9 and abs(bb - a_) > 1e-6:
                fam_a += 1
                break
        except (ValueError, OverflowError, ZeroDivisionError):
            pass
ok(fam_a >= 3, f"'a가 교점 x좌표' 제거 → 여러 a에서 해 존재 ({fam_a}개 a 값에서 확인, 연속 해족)")
fam_b = 0
for b_ in [0.25, 1.0, 1.5, 2.0, 3.0]:
    a_ = 9 - b_  # f(a)=g(a)  <=>  a+b = 9 (오른쪽 가지)
    if abs(h(a_, a_, b_)) < 1e-9:
        S2 = intersections(a_, b_)
        if any(s < 0 and abs(s - a_) > 1e-6 for s in S2):
            fam_b += 1
ok(fam_b >= 3, f"'b가 교점 x좌표' 제거 → a+b=9 위의 여러 (a,b)가 남음 ({fam_b}개 확인)")

# (d) 대표 오답 값
deg = Fraction(9, 2) ** 2 * 2
ok(deg.numerator + deg.denominator == 83 and 83 != ans, "오답 경로 a=b=9/2 → 83 (정답과 다름)")
alt = [(x, y) for x, y in noneg if abs(x - a) > 1e-6]
ok(all(abs(x * x + y * y - round(x * x + y * y)) > 1e-3 for x, y in alt), "오답 경로 (나) 무시 후보 → a^2+b^2 비유리수(정수화 불가)")

print()
print("모두 통과" if fails == 0 else f"실패 {fails}건")
sys.exit(1 if fails else 0)
