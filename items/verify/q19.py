"""q19 검증: 사인법칙·코사인법칙 (원에 내접하는 삼각형, 호의 중점).

문항: 원 O에 내접하는 삼각형 ABC에서 AB=6, AC=4.
점 A를 포함하지 않는 호 BC 위의 점 D가 ∠DBC=∠DCB, AD=3√3을 만족할 때 원 O의 반지름은?
정답 ④ 9√2/4.

검사 (풀이 식을 옮기지 않고 좌표로 독립 계산):
 (a) 정답: ∠A를 매개변수로 삼각형을 만들고 외접원·점 D를 직접 구성, AD=3√3인 근을 고정밀로 찾아 R 비교 + 정확값(sympy) 재확인
 (b) 유일성: ∠A∈(0,π) 전 구간 탐색에서 근이 정확히 하나
 (c) 조건 필요성: 각 조건을 하나씩 빼면 R이 둘 이상의 값을 가짐
 (d) 선지: 오답 경로 값이 선지와 일치, 정답과 겹치지 않음, 오름차순에서 정답이 ④
"""
import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
AB, AC = 6, 4
AD = 3 * mp.sqrt(3)
ANS = sp.Rational(9, 4) * sp.sqrt(2)
fails = []


def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


def build(A, b=AB, c=AC):
    """A=(0,0), B=(b,0), C=(c cosA, c sinA). 외접원 중심·반지름, 호 BC의 두 중점 반환."""
    B = mp.matrix([b, 0]); C = mp.matrix([c * mp.cos(A), c * mp.sin(A)])
    # 외접원 중심: x=b/2, |O|=|O-C|
    ox = mp.mpf(b) / 2
    oy = (c * c - 2 * ox * C[0]) / (2 * C[1])
    O = mp.matrix([ox, oy]); R = mp.sqrt(ox**2 + oy**2)
    M = (B + C) / 2; v = M - O
    if mp.norm(v) < mp.mpf(10)**-20:  # BC가 지름(∠A=90°): BC의 법선 방향
        v = mp.matrix([-(C[1] - B[1]), C[0] - B[0]])
    v = v / mp.norm(v)
    P1, P2 = O + R * v, O - R * v
    side = lambda P: (C[0]-B[0])*(P[1]-B[1]) - (C[1]-B[1])*(P[0]-B[0])
    sA = side(mp.matrix([0, 0]))
    Dn, Dy = (P1, P2) if side(P1) * sA < 0 else (P2, P1)
    return dict(B=B, C=C, O=O, R=R, Dnot=Dn, Dyes=Dy)


def roots(f, N=4000):
    out = []
    xs = [mp.pi * i / N for i in range(1, N)]
    vals = [f(x) for x in xs]
    for i in range(len(xs) - 1):
        if vals[i] == 0 or vals[i] * vals[i + 1] < 0:
            out.append(mp.findroot(f, (xs[i], xs[i + 1]), solver='bisect'))
    return out


def ang(P, Q, S):  # ∠PQS
    u = P - Q; w = S - Q
    return mp.acos((u[0]*w[0] + u[1]*w[1]) / (mp.norm(u) * mp.norm(w)))


# (a)(b) 의도한 배치: D는 A를 포함하지 않는 호 BC의 중점(∠DBC=∠DCB ⇔ DB=DC)
f_not = lambda A: mp.norm(build(A)['Dnot']) - AD
r_not = roots(f_not)
check("(b) 유일성: 조건을 만족하는 삼각형이 하나 (근 %d개)" % len(r_not), len(r_not) == 1)
A0 = r_not[0]; g = build(A0)
D = g['Dnot']
check("(a) 구성 확인: ∠DBC=∠DCB", abs(ang(D, g['B'], g['C']) - ang(D, g['C'], g['B'])) < mp.mpf(10)**-25)
check("(a) 구성 확인: D가 원 위", abs(mp.norm(D - g['O']) - g['R']) < mp.mpf(10)**-25)
check("(a) 정답 R = 9√2/4 (수치 %s)" % mp.nstr(g['R'], 15), abs(g['R'] - mp.mpf(9) / 4 * mp.sqrt(2)) < mp.mpf(10)**-25)
check("(a) cos A = 23/27", abs(mp.cos(A0) - mp.mpf(23) / 27) < mp.mpf(10)**-25)

# 정확값(sympy): cos A = 23/27일 때 외접원·D를 정확히 구성
cA = sp.Rational(23, 27); sA = sp.sqrt(1 - cA**2)
Bx, Cx, Cy = sp.Integer(AB), AC * cA, AC * sA
ox = Bx / 2; oy = sp.nsimplify((AC**2 - 2 * ox * Cx) / (2 * Cy))
R = sp.sqrt(ox**2 + oy**2)
Mx, My = (Bx + Cx) / 2, Cy / 2
vx, vy = Mx - ox, My - oy; n = sp.sqrt(vx**2 + vy**2)
cands = [(ox + s * R * vx / n, oy + s * R * vy / n) for s in (1, -1)]
side = lambda x, y: (Cx - Bx) * (y - 0) - (Cy - 0) * (x - Bx)
Dx, Dy = [p for p in cands if sp.sign(sp.simplify(side(*p))) != sp.sign(sp.simplify(side(0, 0)))][0]
check("(a) 정확값: AD^2 = 27", sp.simplify(Dx**2 + Dy**2 - 27) == 0)
check("(a) 정확값: BD = CD = √3", sp.simplify((Dx-Bx)**2 + Dy**2 - 3) == 0 and sp.simplify((Dx-Cx)**2 + (Dy-Cy)**2 - 3) == 0)
check("(a) 정확값: BC = 10/3", sp.simplify((Bx-Cx)**2 + Cy**2 - sp.Rational(100, 9)) == 0)
check("(a) 정확값: R = 9√2/4", sp.simplify(R - ANS) == 0)

# (c) 조건 필요성
Rs = lambda lst: sorted({mp.nstr(x, 12) for x in lst})
# 단서(호 선택) 제거: A를 포함하는 호의 중점도 허용
f_yes = lambda A: mp.norm(build(A)['Dyes']) - AD
r_yes = roots(f_yes)
R_wo_hint = Rs([build(A)['R'] for A in r_not + r_yes])
check("(c) 단서 제거 → R 후보 %s" % R_wo_hint, len(R_wo_hint) >= 2)
R_trap = build(r_yes[0])['R']
check("(c) 단서 무시 경로 값 = 9√442/52 (선지 밖)", abs(R_trap - mp.mpf(9) * mp.sqrt(442) / 52) < mp.mpf(10)**-25)
# ∠DBC=∠DCB 제거: D가 호 BC(A 미포함) 위 아무 점, AD=3√3 → 여러 삼각형에서 해가 존재
vals = []
for A in [mp.mpf(x) / 10 for x in range(3, 12)]:
    h = build(A); O, Rr = h['O'], h['R']
    # 원 위 점 O + R(cos t, sin t) 중 A 반대쪽 호 위, |D| = AD 인 점 존재 여부
    side2 = lambda P: (h['C'][0]-h['B'][0])*(P[1]-h['B'][1]) - (h['C'][1]-h['B'][1])*(P[0]-h['B'][0])
    sA0 = side2(mp.matrix([0, 0]))
    found = False
    for k in range(2000):
        t = 2 * mp.pi * k / 2000
        P = O + Rr * mp.matrix([mp.cos(t), mp.sin(t)])
        if side2(P) * sA0 < 0 and abs(mp.norm(P) - AD) < mp.mpf('0.02'):
            found = True; break
    if found:
        vals.append(Rr)
check("(c) ∠DBC=∠DCB 제거 → R이 여러 값 (%d개)" % len(Rs(vals)), len(Rs(vals)) >= 2)
# AD=3√3 제거
check("(c) AD 조건 제거 → R이 여러 값", len(Rs([build(mp.mpf(x) / 10)['R'] for x in (4, 6, 8)])) >= 2)
# AB 또는 AC 제거: 다른 AB(AC)로도 AD=3√3 배치가 생기고 R이 달라짐
def R_for(b, c):
    rr = roots(lambda A: mp.norm(build(A, b, c)['Dnot']) - AD, 800)
    return [build(A, b, c)['R'] for A in rr]
alt = R_for(5, 4) + R_for(6, 3) + R_for(6, 4)
check("(c) AB·AC 중 하나를 바꾸면 R이 달라짐 %s" % Rs(alt), len(Rs(alt)) >= 3)

# (d) 선지와 오답 경로
s3 = sp.sqrt(3)
cos_t = sp.Rational(5, 9) * s3                 # ∠BAD=θ
sin_t = sp.sqrt(1 - cos_t**2)
BD = sp.sqrt(sp.Integer(3))
paths = {
    "정답 BD/(2 sinθ)": BD / (2 * sin_t),
    "sinθ 대신 cosθ": BD / (2 * cos_t),
    "BD에서 멈춤": BD,
    "AD를 지름으로 착각(R=AD/2)": 3 * s3 / 2,
    "1/2 빠뜨림(2R)": BD / sin_t,
}
choices = [sp.Rational(9, 10), s3, 3 * s3 / 2, ANS, 9 * sp.sqrt(2) / 2]
for k, v in paths.items():
    print("   경로 %-24s → %s" % (k, sp.nsimplify(sp.radsimp(v))))
check("(d) 정답 경로 = 9√2/4", sp.simplify(paths["정답 BD/(2 sinθ)"] - ANS) == 0)
check("(d) 오답 경로 값이 모두 선지에 있음",
      all(any(sp.simplify(v - c) == 0 for c in choices) for v in paths.values()))
check("(d) 선지 5개 서로 다름", len({sp.N(c, 30) for c in choices}) == 5)
check("(d) 선지 오름차순", all(sp.N(choices[i]) < sp.N(choices[i + 1]) for i in range(4)))
check("(d) 정답 위치 ④", sp.simplify(choices[3] - ANS) == 0)
check("(d) 단서 무시 값은 선지 밖", all(abs(sp.N(c, 30) - R_trap) > 1e-6 for c in choices))

print("\n정답: ④ 9√2/4")
if fails:
    print("FAILED:", fails); sys.exit(1)
print("ALL PASS")
