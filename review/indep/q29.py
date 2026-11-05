"""q29 독립 재계산(3차, M1-8 이후 문항): A=흰1·검1, B=흰1·검2. 공에 이름을 붙여 3회 시행 (2·3)^3 경로 전수."""
from fractions import Fraction as F
start = (('W1', 'K1'), ('W2', 'K2', 'K3'))
paths = [(start, F(1), False)]
for _ in range(3):
    new = []
    for (A, B), p, diff in paths:
        for i in range(len(A)):
            for j in range(len(B)):
                a, b = A[i], B[j]
                nA = tuple(sorted(A[:i] + A[i+1:] + (b,)))
                nB = tuple(sorted(B[:j] + B[j+1:] + (a,)))
                new.append(((nA, nB), p / (len(A) * len(B)), diff or a[0] != b[0]))
    paths = new
cond = [(p, d) for (A, B), p, d in paths if sum(x[0] == 'W' for x in A) == 1]
den = sum(p for p, d in cond); num = sum(p for p, d in cond if d)
r = num / den
print("q29: P(A흰=1) =", den, " 조건부확률 =", r, " p+q =", r.numerator + r.denominator)
assert r.numerator + r.denominator == 227
