#!/usr/bin/env python3
"""items/q*.md + answers.md -> typeset/build/{exam,answers}.tex

문항 파일에서 '## 문항'과 '## 선지' 절만 읽는다. 정답·해설·출제 의도·검증,
그림 메모(조판용)·좌표 줄·'검수 전 대비 변경' 줄은 싣지 않는다.
레이아웃: analysis/2028-example.md §3 (A3, 2단, 머리말/꼬리말, 문항 배치표).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "items"
BUILD = ROOT / "typeset" / "build"

TOTAL_PAGES = 12
# analysis/2028-example.md §3.4 문항 배치 (쪽: (왼쪽 단, 오른쪽 단))
LAYOUT = {
    1: ([1, 2], [3, 4]), 2: ([5, 6], [7]), 3: ([8, 9], [10]),
    4: ([11], [12]), 5: ([13], [14]), 6: ([15], [16]), 7: ([17], [18]),
    8: ([19], [20]), 9: ([21], [22, 23]), 10: ([24, 25], [26]),
    11: ([27], [28]), 12: ([29], [30]),
}
SECTION_BEFORE = {1: "5지선다형", 22: "단답형"}
FIGS = {17: "fig-q17.pdf", 19: "fig-q19.pdf", 29: "q29"}  # q29는 TikZ로 새로 그림
FIG_WIDTH = {17: "0.72", 19: "0.66"}
# 그림 글자 손질(사본에만 적용, items/fig 원본은 그대로): §3.9 영역·직선·원 이름은 이탤릭, 점 이름은 정체
SVG_ITALIC = {17: {"A", "B", "l", "y=mx"}, 19: {"O"}}
SVG_SCALE_FONT = {17: 1.25, 19: 1.15}
SKIP_PREFIXES = ("그림 메모", "그림:", "그림(", "좌표(", "- 검수 전 대비 변경", "검수 전 대비 변경")
CIRCLED = "①②③④⑤"

HANGUL = re.compile(r"[\uac00-\ud7a3]+")


def section(md, name):
    m = re.search(rf"^## {name}\s*$(.*?)(?=^## |\Z)", md, re.S | re.M)
    return m.group(1).strip("\n") if m else ""


def fix_math(m):
    """수식 안 손질: \\boxed{(가)} -> 빈칸 상자, 남은 한글은 \\text{}."""
    m = re.sub(r"\\boxed\{\(([가-힣])\)\}", r"\\blank{\1}", m)
    out, depth = [], 0
    # \blank{가} 안의 한글은 그대로 두고 나머지 한글만 감싼다
    parts = re.split(r"(\\blank\{[가-힣]\})", m)
    for p in parts:
        if p.startswith("\\blank"):
            out.append(p)
        else:
            out.append(HANGUL.sub(lambda h: r"\text{" + h.group(0) + "}", p))
    return "".join(out)


def inline(text):
    """한 줄 본문(markdown) -> LaTeX. $...$ 는 수식, 나머지는 글."""
    text = text.replace("\u3000", " ")
    pieces = re.split(r"(\$\$.*?\$\$|\$.*?\$)", text)
    out = []
    for p in pieces:
        if p.startswith("$$"):
            out.append("$\\displaystyle " + fix_math(p[2:-2]) + "$")
        elif p.startswith("$"):
            out.append("$" + fix_math(p[1:-1]) + "$")
        else:
            p = p.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
            p = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", p)
            # 배점 [n점]은 본문 끝에 이어 쓴다
            p = re.sub(r"\[(\d)점\]", r"\\pts{\1}", p)
            out.append(p)
    s = "".join(out)
    # 숫자와 조사 사이: '$400$ 명' 처럼 원문에 띄운 곳은 그대로 둔다(문항 원문 존중)
    return s.strip()


def display(line):
    """독립 수식 줄 (§3.5: 단 폭 약 10% 들여 쓴 왼쪽 정렬)."""
    line = line.strip().replace("\u3000", " ").strip()
    if line.startswith("$$") and line.endswith("$$"):
        body = line[2:-2]
    elif line.startswith("$") and line.endswith("$") and line.count("$") == 2:
        body = line[1:-1]
    else:  # 수식과 글이 섞인 들여 쓴 줄
        return "\\dline{" + inline(line) + "}"
    body = body.replace(r",\quad", r",\qquad")
    return "\\dline{$\\displaystyle " + fix_math(body) + "$}"


def is_display(line):
    s = line.strip()
    return (s.startswith("$$") and s.endswith("$$") and len(s) > 4) or line.startswith("\u3000")


def table(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]
    ncol = len(rows[0])
    out = ["\\begin{center}\\renewcommand{\\arraystretch}{1.25}",
           "\\begin{tabular}{|" + "|".join(["c"] * ncol) + "|}\\hline"]
    for r in rows:
        out.append(" & ".join(inline(c) for c in r) + " \\\\\\hline")
    out.append("\\end{tabular}\\end{center}")
    return "\n".join(out)


def condbox(lines):
    """> 인용 블록. 수식 하나뿐이면 독립 수식 줄, 아니면 조건 상자."""
    body = [l[1:].strip() if l.startswith(">") else l for l in lines]
    body = [b for b in body if b]
    if len(body) == 1 and body[0].startswith("$$"):
        return display(body[0])
    out = []
    for b in body:
        m = re.match(r"^\(([가-힣])\)\s*(.*)$", b)
        if b.startswith("$$"):
            out.append(display(b))
        elif m:
            out.append("\\cond{" + m.group(1) + "}{" + inline(m.group(2)) + "}")
        else:
            out.append("\\condtext{" + inline(b) + "}")
    return "\\begin{condbox}\n" + "\n".join(out) + "\n\\end{condbox}"


def stem(md_text):
    """'## 문항' 절 -> LaTeX 블록 목록."""
    lines = md_text.split("\n")
    blocks, para = [], []

    def flush():
        if para:
            blocks.append(("p", " ".join(inline(x) for x in para)))
            para.clear()

    i = 0
    while i < len(lines):
        l = lines[i]
        s = l.strip()
        if not s:
            flush(); i += 1; continue
        if s.startswith(SKIP_PREFIXES):
            flush()
            while i < len(lines) and lines[i].strip():
                i += 1
            continue
        if s.startswith(">"):
            flush()
            q = []
            while i < len(lines) and (lines[i].strip().startswith(">")):
                q.append(lines[i].strip()); i += 1
            blocks.append(("box", condbox(q)))
            continue
        if s.startswith("|"):
            flush()
            t = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                t.append(lines[i]); i += 1
            blocks.append(("table", table(t)))
            continue
        if is_display(l):
            flush()
            blocks.append(("disp", display(l)))
            i += 1; continue
        para.append(s); i += 1
    flush()
    # 따로 떨어진 '[n점]'만 있는 문단은 앞 글 문단 끝으로 옮긴다(§3.5 배점은 발문 끝)
    for k, (kind, txt) in enumerate(blocks):
        if kind == "p" and re.fullmatch(r"\\pts\{\d\}", txt):
            for j in range(k - 1, -1, -1):
                if blocks[j][0] == "p":
                    blocks[j] = ("p", blocks[j][1] + " " + txt)
                    break
            blocks[k] = ("drop", "")
    return [b for b in blocks if b[0] != "drop"]


def parse_choices(text):
    t = text.strip().replace("\u3000", " ")
    if not t or t.startswith("단답형"):
        return None
    parts = re.split(r"([①②③④⑤])", t)
    ch = {}
    for k in range(1, len(parts) - 1, 2):
        ch[parts[k]] = parts[k + 1].strip()
    vals = [ch[c] for c in CIRCLED]
    out = []
    for v in vals:
        if v.startswith("$") and v.endswith("$"):
            v = v[1:-1]
        out.append(v)
    return out


def load_item(n):
    md = (ITEMS / f"q{n}.md").read_text(encoding="utf-8")
    st = section(md, "문항")
    ch = parse_choices(section(md, "선지"))
    pts = re.search(r"\[(\d)점\]", st)
    return {"n": n, "blocks": stem(st), "choices": ch, "points": int(pts.group(1))}


def item_tex(it):
    n = it["n"]
    out = []
    if n in SECTION_BEFORE:
        out.append("\\sectionlabel{" + "\\hspace{3bp}".join(SECTION_BEFORE[n]) + "}")
    out.append("\\begin{qitem}{" + str(n) + "}")
    first = True
    for kind, txt in it["blocks"]:
        if kind == "p":
            out.append(("" if first else "\\par ") + txt)
        else:
            out.append(txt)
        first = False
    fig = FIGS.get(n)
    if fig == "q29":
        out.append("\\figpouches")
    elif fig:
        out.append("\\qfig{" + FIG_WIDTH[n] + "}{" + fig + "}")
    if it["choices"]:
        cmd = "\\choicesfrac{" if any("frac" in c for c in it["choices"]) else "\\choices{"
        out.append(cmd + "}{".join(fix_math(c) for c in it["choices"]) + "}")
    out.append("\\end{qitem}")
    return "\n".join(out)


def exam_tex(items):
    pages = []
    for p in range(1, TOTAL_PAGES + 1):
        left, right = LAYOUT[p]
        cols = []
        for side, nums in (("L", left), ("R", right)):
            bodies = ["{" + item_tex(items[n]) + "}" for n in nums]
            last = (p == TOTAL_PAGES and side == "R")
            if len(bodies) == 1:
                cols.append(f"\\colone{{{side}}}{{{nums[0]}}}{bodies[0]}{{{'1' if last else '0'}}}")
            else:
                cols.append(f"\\coltwo{{{side}}}{{{nums[0]}}}{{{nums[1]}}}{bodies[0]}{bodies[1]}")
        pages.append(f"\\exampage{{{p}}}{{\n" + "\n".join(cols) + "\n}")
    pre = (ROOT / "typeset" / "exam-preamble.tex").read_text(encoding="utf-8")
    return pre + "\n\\begin{document}\n" + "\n".join(pages) + "\n\\end{document}\n"


def parse_answers():
    md = (ROOT / "answers.md").read_text(encoding="utf-8")
    rows = {}
    for l in md.split("\n"):
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) == 6 and cells[0].isdigit():
            for k in (0, 3):
                rows[int(cells[k])] = (cells[k + 1], int(cells[k + 2]))
    return rows


def answers_tex(ans):
    pre = (ROOT / "typeset" / "answers-preamble.tex").read_text(encoding="utf-8")
    def row(n):
        a, p = ans[n]
        a = a if a in CIRCLED else f"${a}$"
        return f"{n} & {a} & {p}"
    lines = [row(n) + " & " + row(n + 15) + r" \\ \hline" for n in range(1, 16)]
    total = sum(p for _, p in ans.values())
    return pre + "\\begin{document}\n\\answersheet{" + "\n".join(lines) + "}{" + str(total) + "}\n\\end{document}\n"


def prepare_svgs():
    for n, ital in SVG_ITALIC.items():
        svg = (ITEMS / "fig" / f"q{n}.svg").read_text(encoding="utf-8")
        k = SVG_SCALE_FONT[n]
        svg = re.sub(r'font-size="(\d+(?:\.\d+)?)"', lambda m: f'font-size="{float(m.group(1)) * k:g}"', svg)
        svg = svg.replace('font-family="serif"', 'font-family="Latin Modern Roman, serif"')
        svg = re.sub(r"<text([^>]*)>([^<]+)</text>",
                     lambda m: f'<text{m.group(1)}{" font-style=\"italic\"" if m.group(2) in ital else ""}>{m.group(2)}</text>', svg)
        (BUILD / f"fig-q{n}.svg").write_text(svg, encoding="utf-8")


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    prepare_svgs()
    items = {n: load_item(n) for n in range(1, 31)}
    (BUILD / "exam.tex").write_text(exam_tex(items), encoding="utf-8")
    ans = parse_answers()
    (BUILD / "answers.tex").write_text(answers_tex(ans), encoding="utf-8")
    # 대조 스크립트(check.py)가 쓰는 조판 기준값
    dump = {n: {"choices": it["choices"], "points": it["points"]} for n, it in items.items()}
    (BUILD / "typeset-data.json").write_text(json.dumps(dump, ensure_ascii=False, indent=1), encoding="utf-8")
    print("make_tex: exam.tex, answers.tex 생성")


if __name__ == "__main__":
    sys.exit(main())
