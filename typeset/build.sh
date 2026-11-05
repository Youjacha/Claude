#!/usr/bin/env bash
# 문제지·정답표 재생성: bash typeset/build.sh  →  out/mock-exam.pdf, out/exam.pdf, out/answers.pdf
# 필요: texlive-xetex texlive-lang-korean texlive-latex-extra texlive-pictures fonts-nanum librsvg2-bin poppler-utils
# 단 넘침(OVERFLOW)이나 정답·선지 불일치(check.py)가 있으면 실패한다.
set -euo pipefail
cd "$(dirname "$0")/.."
B=typeset/build
mkdir -p "$B" out
python3 typeset/make_tex.py
for q in 17 19; do rsvg-convert -f pdf -o "$B/fig-q$q.pdf" "$B/fig-q$q.svg"; done
cd "$B"
for t in exam answers; do
  for pass in 1 2; do xelatex -interaction=nonstopmode -halt-on-error "$t.tex" >/dev/null || { tail -40 "$t.log"; exit 1; }; done
done
cd - >/dev/null
if grep -q '^OVERFLOW' "$B/exam.log"; then grep '^OVERFLOW' "$B/exam.log"; echo "단 넘침 있음" >&2; exit 1; fi
cp "$B/exam.pdf" out/mock-exam.pdf
cp "$B/exam.pdf" out/exam.pdf
cp "$B/answers.pdf" out/answers.pdf
python3 typeset/check.py
