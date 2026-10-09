#!/usr/bin/env bash
set -euo pipefail

doc_path="$1"
doc_dir="$(cd "$(dirname "$doc_path")" && pwd)"
doc_name="$(basename "$doc_path" .tex)"
build_dir="$doc_dir/build"

mkdir -p "$build_dir"
latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf \
  -outdir="$build_dir" "$doc_path"
cp "$build_dir/$doc_name.pdf" "$doc_dir/$doc_name.pdf"
