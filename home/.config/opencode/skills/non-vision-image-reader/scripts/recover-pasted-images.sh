#!/usr/bin/env bash
# Recover images pasted into the current opencode prompt (for non-vision models).
# opencode stores each pasted image in its session SQLite DB as a base64 data URL.
# All images of one user message share a message_id; pull the most recent user
# message's images, ordered by part id, into image-1.png, image-2.png, ...
# Prints one image file path per line on success; exits non-zero if none found.
set -euo pipefail

DB="${XDG_DATA_HOME:-$HOME/.local/share}/opencode/opencode.db"
if [[ ! -f "$DB" ]]; then
  echo "ERROR: opencode DB not found at $DB" >&2
  exit 1
fi

TMP="$(mktemp -d)"

MSGID=$(sqlite3 "$DB" "
SELECT p.message_id
FROM part p JOIN message m ON m.id = p.message_id
WHERE json_extract(m.data,'\$.role')='user'
  AND json_extract(p.data,'\$.type')='file'
  AND json_extract(p.data,'\$.mime') LIKE 'image/%'
ORDER BY p.time_created DESC LIMIT 1;")

if [[ -z "${MSGID:-}" ]]; then
  echo "ERROR: no pasted images found for the current prompt." >&2
  rm -rf "$TMP"
  exit 1
fi

if [[ ! "$MSGID" =~ ^[A-Za-z0-9_-]+$ ]]; then
  echo "ERROR: unexpected message_id format: $MSGID" >&2
  rm -rf "$TMP"
  exit 1
fi

i=0
paths=()
while IFS= read -r url; do
  i=$((i+1))
  out="$TMP/image-$i.png"
  printf '%s' "${url#*base64,}" | base64 -d > "$out"
  paths+=("$out")
done < <(sqlite3 "$DB" "
SELECT json_extract(data,'\$.url')
FROM part
WHERE message_id='$MSGID'
  AND json_extract(data,'\$.type')='file'
  AND json_extract(data,'\$.mime') LIKE 'image/%'
ORDER BY id ASC;")

if (( ${#paths[@]} == 0 )); then
  echo "ERROR: no image parts decoded for message $MSGID." >&2
  rm -rf "$TMP"
  exit 1
fi

printf '%s\n' "${paths[@]}"
