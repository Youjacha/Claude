#!/usr/bin/env python3
"""조판 결과 대조: items 정답 ↔ answers.md ↔ 문제지에 실린 선지·배점, PDF 쪽수·금지 문구."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CIRCLED = "①②③④⑤"
errors = []


def norm(s):
    s = s.strip().strip("$").replace(" ", "")
    s = re.sub(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\sqrt\{?(\d+)\}?", r"√\1", s)
    s = s.replace("−", "-").replace("{", "").replace("}", "")
    s = re.sub(r"\(([^()]+)\)/", r"\1/", s)
    s = re.sub(r"/\(([^()]+)\)", r"/\1", s)
    return s


md = (ROOT / "answers.md").read_text(encoding="utf-8")
ans, vals = {}, {}
for l in md.split("\n"):
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if len(c) == 6 and c[0].isdigit():
        for k in (0, 3):
            ans[int(c[k])] = (c[k + 1], int(c[k + 2]))
    elif len(c) == 3 and c[0].isdigit() and c[1] in CIRCLED:
        vals[int(c[0])] = c[2]
if sorted(ans) != list(range(1, 31)):
    errors.append(f"answers.md 정답표 번호 누락: {sorted(set(range(1, 31)) - set(ans))}")

data = json.loads((ROOT / "typeset" / "build" / "typeset-data.json").read_text(encoding="utf-8"))
for n in range(1, 31):
    item = (ROOT / "items" / f"q{n}.md").read_text(encoding="utf-8")
    m = re.search(r"^## 정답\s*\n+(.+)$", item, re.M)
    line = m.group(1).strip()
    a, pts = ans[n]
    d = data[str(n)]
    if d["points"] != pts:
        errors.append(f"q{n}: 배점 문제지 {d['points']} / answers.md {pts}")
    if n <= 21:
        no, val = line[0], line[1:].strip()
        if no != a:
            errors.append(f"q{n}: 정답 번호 items {no} / answers.md {a}")
        ch = d["choices"]
        if not ch or len(ch) != 5:
            errors.append(f"q{n}: 선지 5개가 아님")
            continue
        printed = ch[CIRCLED.index(a)]
        if norm(printed) != norm(val):
            errors.append(f"q{n}: 문제지 {a} 선지 '{printed}' ≠ items 정답 값 '{val}'")
        if n in vals and norm(vals[n]) != norm(val):
            errors.append(f"q{n}: answers.md 값 '{vals[n]}' ≠ items '{val}'")
        if len({norm(x) for x in ch}) != 5:
            errors.append(f"q{n}: 선지 중복")
    else:
        if d["choices"] is not None:
            errors.append(f"q{n}: 단답형인데 선지가 실림")
        if norm(line) != a:
            errors.append(f"q{n}: 단답 정답 items '{line}' / answers.md '{a}'")

out = ROOT / "out"
for pdf, pages in (("mock-exam.pdf", 12), ("answers.pdf", 1)):
    info = subprocess.run(["pdfinfo", str(out / pdf)], capture_output=True, text=True).stdout
    got = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    if got != pages:
        errors.append(f"{pdf}: {got}쪽 (기대 {pages}쪽)")

text = subprocess.run(["pdftotext", "-layout", str(out / "mock-exam.pdf"), "-"], capture_output=True, text=True).stdout
for bad in ("정답", "해설", "그림 메모", "좌표(", "검수", "출제 의도", "조판용", "items/"):
    if bad in text:
        errors.append(f"문제지에 실리면 안 되는 문구: '{bad}'")
for k, cnt in ((2, 3), (3, 14), (4, 13)):
    got = text.count(f"[{k}점]")
    if got != cnt:
        errors.append(f"문제지 [{k}점] {got}개 (기대 {cnt})")
for n in range(1, 31):
    if not re.search(rf"(^|\s){n}\.\s", text):
        errors.append(f"문제지에서 문항 번호 {n}. 을 찾지 못함")

atext = subprocess.run(["pdftotext", "-layout", str(out / "answers.pdf"), "-"], capture_output=True, text=True).stdout
for n, (a, p) in ans.items():
    if not re.search(rf"(^|\s){n}\s+{re.escape(a)}\s+{p}(\s|$)", atext, re.M):
        errors.append(f"answers.pdf: {n}번 행 '{n} {a} {p}' 없음")

if errors:
    print("check: 불일치", len(errors))
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("check: 통과 — 30문항 정답·선지·배점 일치, 문제지 12쪽, 정답표 1쪽")
