#!/bin/bash
set -euo pipefail

if [[ $# -ne 2 || -z "$1" || -z "$2" ]]; then
    echo "Usage: bash get_books.sh BUCKET BOOK_DIR" >&2
    exit 2
fi

bucket=$1
book_dir=$2

mkdir -p "$book_dir"
book_dir=$(realpath "$book_dir")

aws s3 cp "s3://$bucket/" "$book_dir/" \
    --recursive \
    --exclude "*" \
    --include "*.txt"

book_list="$PWD/book_list.txt"
printf 'File path\n' > "$book_list"
find "$book_dir" -type f -name '*.txt' -print | LC_ALL=C sort >> "$book_list"

book_count=$(($(wc -l < "$book_list") - 1))
echo "Wrote $book_count book files to book_list.txt"
