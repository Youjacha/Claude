# 검증 스크립트

`analysis/discrimination/*.md`의 정답, 오답 값, 재사용 템플릿 수치를 다시 계산하는 스크립트이다.

## 준비

```bash
pip install sympy numpy mpmath
```

## 실행 (저장소 루트에서)

| 스크립트 | 대상 문서 | 필요 패키지 | 실행 시간(참고) |
|---|---|---|---|
| `verify_2028.py` | `../2028-example.md` | sympy, mpmath | 약 3분 |
| `verify_2027-06.py` | `../2027-06.md` | sympy, numpy | 약 40초 |
| `2027-09_verify.py` | `../2027-09.md` | sympy, numpy | 약 20초 |
| `2026-csat_verify.py` | `../2026-csat.md` | sympy | 약 30초 |

```bash
python3 -I analysis/discrimination/scripts/verify_2028.py
python3 -I analysis/discrimination/scripts/verify_2027-06.py
python3 -I analysis/discrimination/scripts/2027-09_verify.py
python3 -I analysis/discrimination/scripts/2026-csat_verify.py
```

- 각 스크립트는 문항별 정답(`Q..`/`== ..`)과 템플릿 수치(`T..`)를 출력한다. 출력값을 해당 문서의 부록과 비교하면 된다.
- 2026-11-04에 네 스크립트를 모두 실행했다. 모두 종료 코드 0이었고, 출력이 각 문서의 정답·템플릿 수치와 일치했다.
- 새 4점 문항을 만들 때도 같은 방식으로 `scripts/`에 검증 스크립트를 둔다. 체크리스트는 `../README.md` §4에 있다.
