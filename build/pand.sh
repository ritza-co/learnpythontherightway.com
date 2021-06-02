#!/bin/bash
cp "$1" "in.md"
# sed -i '' 's_\(^!\[.*\](\)_\1https://i.ritzastatic.com/learn-python-the-right-way/_' in.md

pandoc "in.md" --no-highlight -f markdown-auto_identifiers-citations -t html --lua-filter assets/fix-pre-code.lua -o out-temp.html

cat assets/template_pre.html out-temp.html assets/template_post.html > out.html
