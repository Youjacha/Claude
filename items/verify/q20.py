#!/usr/bin/env python3
"""q20 검증 스크립트 (미적분Ⅰ · 정적분으로 정의된 함수, 5지선다, 정답 ① 9).

문항 요약
  f: 최고차항 계수 양수인 삼차함수, f(α)=f(β)=f(γ)=0 (α<0<β<γ)
  g(x)=∫_0^x f,  h(x)=∫_0^x |f|
  (가) 방정식 g(x)=0의 서로 다른 실근의 개수는 3
  (나) 방정식 g(x)=-1의 서로 다른 실근의 개수는 1
  (다) ∫_α^γ |f(x)| dx = 11
  묻는 값: h(α)+h(γ)

방법 (풀이의 넓이 장부를 쓰지 않는 독립 계산)
  x -> Lx 확대와 계수 조정으로 β=1로 정규화한다(조건 (가)(나)(다)와 묻는 값은
  이 변환에서 c·L^4 배로만 바뀌므로 일반성을 잃지 않는다).
  f(x) = c·s·(x-a)(x-1)(x-r), c>0, s=±1 (최고차항 부호).
  (가)는 '사차함수 g가 중근을 가짐' ⇔ 어떤 임계점 p∈{a,1,r}에서 g(p)=0 이므로
  세 후보 곡선 각각을 만든다. (나)는 'g(x)+1이 중근을 가짐' ⇔ 어떤 임계점 q에서
  c·g₁(q)=-1 (g₁은 c=1인 모델)이고, (다)는 c·H=11이므로 c를 지우면 11·g₁(q)+H=0.
  두 곡선을 종결식(resultant)으로 연립해 모든 해를 구한다. 각 해에서 g=0, g=-1의
  실근 개수를 수치로 다시 세고,
  묻는 값 h(α)+h(γ)를 |f|의 수치적분(합성 심프슨)으로 직접 계산한다.
"""
import sys
import numpy as np
import sympy as sp

a, r, x = sp.symbols("a r x", real=True)
FAIL = []


def check(name, ok, info=""):
    print(("  [통과] " if ok else "  [실패] ") + name + (f"  {info}" if info else ""))
    if not ok:
        FAIL.append(name)


def model(s):
    """단위 계수(c=1) 모델의 다항식 표현."""
    f = s * (x - a) * (x - 1) * (x - r)
    F = sp.integrate(sp.expand(f), x)
    G = lambda u: sp.expand(F.subs(x, u) - F.subs(x, 0))  # g(u)/c
    E = sp.expand(G(a) + G(1) + G(r))                      # 모든 극값의 합 / c
    I1 = sp.expand(F.subs(x, 1) - F.subs(x, a))            # ∫_a^1 f
    I2 = sp.expand(F.subs(x, r) - F.subs(x, 1))            # ∫_1^r f
    H = sp.expand(s * I1 - s * I2)                         # ∫_α^γ |f| / c  (부호표: (a,1)에서 s, (1,r)에서 -s)
    return f, G, E, H


def num_f(s, av, rv):
    return lambda t: s * (t - av) * (t - 1) * (t - rv)


def simpson(fun, lo, hi, n=20000):
    if lo == hi:
        return 0.0
    t = np.linspace(lo, hi, n + 1)
    y = fun(t)
    return (hi - lo) / (3 * n) * (y[0] + y[-1] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum())


def h_num(s, av, rv, c, u):
    fn = num_f(s, av, rv)
    return c * simpson(lambda t: np.abs(fn(t)), 0.0, u)


def g_num(s, av, rv, c, u):
    return c * simpson(num_f(s, av, rv), 0.0, u)


def distinct_real_roots_g(s, av, rv, c, level=0.0):
    # g(x) = level 의 서로 다른 실근. g(x) = c*s*∫_0^x (t-a)(t-1)(t-r) dt
    p = np.poly1d([1.0, -(av + 1 + rv), av + rv + av * rv, -av * rv])  # (t-a)(t-1)(t-r)
    P = c * s * p.integ() - level                                      # g - level
    roots = np.roots(P.coeffs)
    re = sorted(z.real for z in roots if abs(z.imag) < 1e-4)
    cl = []
    for z in re:
        if not cl or abs(z - cl[-1]) > 1e-3:
            cl.append(z)
    return len(cl), cl


def solve_all(s, region, verbose=False):
    """(가)(나)(다)를 모두 만족시키는 (a, r, c)를 모두 찾는다 (β=1 정규화)."""
    f, G, E, H = model(s)
    crit = (a, sp.Integer(1), r)
    sols = []
    for p in crit:
        Gp = sp.expand(G(p))
        if Gp == 0:
            continue
        for q in crit:
            if q == p:
                continue  # g(p)=0 이면 c·g₁(p)=-1 불가
            Rq = sp.expand(11 * G(q) + H)   # (나) c·g₁(q)=-1, (다) c·H=11
            res = sp.Poly(sp.resultant(sp.Poly(Gp, a), sp.Poly(Rq, a)), r)
            if res.is_zero:
                continue
            rroots = []
            for fac, _m in sp.factor_list(res.as_expr(), r)[1]:
                fp = sp.Poly(fac, r)
                if fp.degree() >= 1:
                    rroots += fp.nroots(n=30, maxsteps=500)
            for rr in rroots:
                if abs(sp.im(rr)) > 1e-12:
                    continue
                rv = float(sp.re(rr))
                pa = sp.Poly(Gp.subs(r, rv), a)
                if pa.degree() < 1:
                    continue
                for aa in pa.nroots(n=30, maxsteps=500):
                    if abs(sp.im(aa)) > 1e-9:
                        continue
                    av = float(sp.re(aa))
                    if abs(float(Rq.subs({a: av, r: rv}))) > 1e-6 * (1 + abs(float(H.subs({a: av, r: rv})))):
                        continue
                    if not region(av, rv):
                        continue
                    Hv = float(H.subs({a: av, r: rv}))
                    if Hv <= 0:
                        continue  # c>0 이 되도록
                    c = 11.0 / Hv
                    n0, _ = distinct_real_roots_g(s, av, rv, c)
                    n1, _ = distinct_real_roots_g(s, av, rv, c, level=-1.0)
                    if n0 != 3 or n1 != 1:
                        continue
                    Q = h_num(s, av, rv, c, av) + h_num(s, av, rv, c, rv)
                    key = (round(av, 8), round(rv, 8))
                    if key not in [(round(t[0], 8), round(t[1], 8)) for t in sols]:
                        sols.append((av, rv, c, Q, str(p), str(q)))
    return sols


print("=" * 64)
print("q20 검증")
print("=" * 64)

# ---------------------------------------------------------------- (a)(b)
print("\n(a)(b) 정답과 유일성 — 최고차항 양수, α<0<β<γ (β=1 정규화)")
main = solve_all(1, lambda av, rv: av < 0 < 1 < rv)
for av, rv, c, Q, p, q in main:
    print(f"    해: α={av:.6f}, β=1, γ={rv:.6f}, c={c:.6f}, (가) 중근 위치={p}, (나) 중근 위치={q}, h(α)+h(γ)={Q:.6f}")
check("해가 존재한다", len(main) >= 1)
Qs = sorted({round(t[3], 6) for t in main})
check("묻는 값이 하나로 정해진다(불변량)", len(Qs) == 1, f"값 집합={Qs}")
check("정답 = 9", len(Qs) == 1 and abs(Qs[0] - 9) < 1e-4)

# 해의 장부 값(참고) 및 수치로 조건 재확인
if main:
    av, rv, c, Q, p, q = main[0]
    gA, gB, gC = (g_num(1, av, rv, c, u) for u in (av, 1.0, rv))
    tot = c * simpson(lambda t: np.abs(num_f(1, av, rv)(t)), av, rv)
    print(f"    g(α)={gA:.6f}, g(β)={gB:.6f}, g(γ)={gC:.6f}, 극값의 합={gA+gB+gC:.6f}, ∫_α^γ|f|={tot:.6f}")
    print(f"    h(α)={h_num(1, av, rv, c, av):.6f}, h(γ)={h_num(1, av, rv, c, rv):.6f}")
    check("수치 재확인: (나) 최솟값 g(α) = -1 (g=-1에 접함)", abs(gA + 1) < 1e-6 and q == "a")
    check("수치 재확인: (다) ∫|f| = 11", abs(tot - 11) < 1e-6)
    check("중근은 γ에서 (g(γ)=0)", p == "r" and abs(gC) < 1e-8)

# 함수는 유일하지 않다: x->Lx 확대족
if main:
    av, rv, c, Q, p, q = main[0]
    vals = []
    for L in (0.5, 1.0, 2.0, 3.7):
        aL, bL, rL, cL = av * L, 1.0 * L, rv * L, c / L ** 4
        fn = lambda t: cL * (t - aL) * (t - bL) * (t - rL)
        hA = simpson(lambda t: np.abs(fn(t)), 0.0, aL)
        hC = simpson(lambda t: np.abs(fn(t)), 0.0, rL)
        vals.append(round(hA + hC, 6))
    check("서로 다른 f(확대족)에서도 h(α)+h(γ)=9", all(abs(v - 9) < 1e-4 for v in vals), f"{vals}")

# (가) 번역의 확인: α<0<β<γ에서 g(x)=0의 근 개수는 g(γ)<0이면 4, >0이면 2
rng = np.random.default_rng(20)
ok = True
for _ in range(2000):
    av = -rng.uniform(0.05, 3)
    rv = 1 + rng.uniform(0.05, 4)
    n, _ = distinct_real_roots_g(1, av, rv, 1.0)
    gc = g_num(1, av, rv, 1.0, rv)
    if abs(gc) < 1e-3:
        continue
    if (gc < 0 and n != 4) or (gc > 0 and n != 2):
        ok = False
        break
check("(가) 번역: 근 개수 3 ⇔ g(γ)=0 (무작위 2000개 표본)", ok)

# ---------------------------------------------------------------- (c)
print("\n(c) 조건 필요성")
f1, G1, E1, H1 = model(1)


def Q_of(av, rv, c):
    return h_num(1, av, rv, c, av) + h_num(1, av, rv, c, rv)


# (가) 제거: (나)(다)와 α<0<1<r 만족 해를 여러 r에서 구해 묻는 값 비교
vals = []
for rv in np.linspace(1.1, 8.0, 70):
    rv = float(rv)
    for qq in (a, sp.Integer(1), r):
        Rq = sp.expand(11 * G1(qq) + H1).subs(r, rv)
        pa = sp.Poly(Rq, a)
        if pa.degree() < 1:
            continue
        for aa in pa.nroots():
            if abs(sp.im(aa)) > 1e-9:
                continue
            av = float(sp.re(aa))
            if not av < 0:
                continue
            Hv = float(H1.subs({a: av, r: rv}))
            if Hv <= 0:
                continue
            c = 11 / Hv
            if distinct_real_roots_g(1, av, rv, c, level=-1.0)[0] == 1:
                vals.append(round(Q_of(av, rv, c), 4))
check("(가)를 빼면 묻는 값이 여러 개", len(set(vals)) >= 2, f"{len(set(vals))}개, 범위 {min(vals)}~{max(vals)}")

# (가)만 둔 곡선 a=a(r) (g(γ)=0): r∈(2,3)에서 α<0
a_of_r = sp.solve(sp.expand(G1(r)), a)[0]
print(f"    (가) 곡선: α = {sp.factor(a_of_r)}  (β=1)")

# (나) 제거: (가)+(다) → c=11/H, r에 따라 값이 바뀜
vals = []
for rv in (2.1, 2.3, 2.6, 2.9):
    av = float(a_of_r.subs(r, rv))
    c = 11 / float(H1.subs({a: av, r: rv}))
    vals.append(round(Q_of(av, rv, c), 4))
check("(나)를 빼면 묻는 값이 여러 개", len(set(vals)) >= 2, f"{vals}")

# (다) 제거: (가)+(나) → 최솟값 g(α)=-1, c=-1/g₁(α)
vals = []
for rv in (2.1, 2.3, 2.6, 2.9):
    av = float(a_of_r.subs(r, rv))
    c = -1 / float(G1(a).subs({a: av, r: rv}))
    vals.append(round(Q_of(av, rv, c), 4))
check("(다)를 빼면 묻는 값이 여러 개", len(set(vals)) >= 2, f"{vals}")

# α<0 제거 (0<α<β<γ 허용): 다른 값이 나온다
alt = solve_all(1, lambda av, rv: 0 < av < 1 < rv)
alt_Q = sorted({round(t[3], 4) for t in alt})
print(f"    0<α<β<γ 의 해: {[(round(t[0],4), round(t[1],4), round(t[3],4)) for t in alt]}")
check("α<0을 빼면(0<α 허용) 답이 9 하나로 정해지지 않음",
      any(abs(q - 9) > 1e-3 for q in alt_Q), f"추가 값={alt_Q}")

# 최고차항 양수 제거 (s=-1, α<0<β<γ 허용)
neg = solve_all(-1, lambda av, rv: av < 0 < 1 < rv)
neg_Q = sorted({round(t[3], 4) for t in neg})
print(f"    최고차항 음수의 해: {[(round(t[0],4), round(t[1],4), round(t[3],4)) for t in neg]}")
# (나) 변경 후: 최고차항이 음수이면 g→-∞ 이므로 g(x)=-1의 근이 항상 2개 이상 → 해 없음.
# 따라서 이 조건은 답을 바꾸는 조건이 아니라 부호표를 고정하는 '풀이 열쇠'이다.
check("최고차항 음수이면 해 없음(풀이 열쇠: 빼도 답 9 유지)", len(neg) == 0, f"음수 해={neg_Q}")

# ---------------------------------------------------------------- (d)
print("\n(d) 선지 검사")
options = [9, 10, 11, 12, 13]
answer_idx = 0
check("선지가 오름차순·등간격·서로 다름", options == sorted(set(options)) and len({b - a_ for a_, b in zip(options, options[1:])}) == 1)
check("정답이 ①", abs(options[answer_idx] - 9) < 1e-9)

# 대표 오답 경로: 넓이 장부 A=∫_α^0 f, B=∫_0^β f, C=∫_β^γ(-f)
A_, B_ = sp.symbols("A B", positive=True)
# 바른 장부: C=B, (나) 최솟값 g(α)=-A=-1, (다) A+2B=11, 묻는 값 h(α)+h(γ) = -A + 2B
sol = sp.solve([A_ - 1, A_ + 2 * B_ - 11], [A_, B_], dict=True)[0]
right = -sol[A_] + 2 * sol[B_]
check("장부 계산과 독립 계산 일치", right == 9, f"A={sol[A_]}, B={sol[B_]}")
# 오답1: h(α)를 넓이(양수) A로 처리 → A + 2B
w1 = sol[A_] + 2 * sol[B_]
# 오답2: h(γ)를 B(양의 조각)만으로 → -A + B
w2 = -sol[A_] + sol[B_]
# 오답3: h를 g처럼 처리 → g(α)+g(γ) = -A + 0
w3 = -sol[A_]
# 오답4: h(α)를 양수로, h(γ)=B만 → A + B
w4 = sol[A_] + sol[B_]
wrong = {"h(α)=+넓이": w1, "h(γ)=B만": w2, "h를 g로": w3, "h(α)=+넓이 & h(γ)=B만": w4}
for k, v in wrong.items():
    print(f"    오답 경로 [{k}] → {v} ({'선지 ' + '①②③④⑤'[options.index(v)] if v in options else '선지 밖'})")
check("오답 값이 정답과 겹치지 않음", all(v != 9 for v in wrong.values()))
check("대표 오답(h(α)=+넓이) 11이 선지 ③에 있음", w1 == 11 and options.index(11) == 2)
# 오답5: (나)를 극솟값 g(γ)=-1로 착각((가)의 접점과 혼동) → (가)와 모순, 해 없음 → 확인
check("(나)를 g(γ)=-1로 읽으면 (가) g(γ)=0과 모순", True)

print("\n" + "=" * 64)
if FAIL:
    print(f"실패 {len(FAIL)}건: {FAIL}")
    sys.exit(1)
print("모두 통과 — 정답 ① 9")
