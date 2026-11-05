#!/usr/bin/env bash
# Usage: bash test_curl.sh KEY_ALICE KEY_BOB KEY_CHARLIE
URL="http://127.0.0.1:5001/process"
H="Content-Type: application/json"
BODY='{"text":"hello rootsoftware"}'

echo "--- Consumer 1 (valid) ---"; curl -s -X POST $URL -H "$H" -H "X-API-Key: $1" -d "$BODY"; echo
echo "--- Consumer 2 (valid) ---"; curl -s -X POST $URL -H "$H" -H "X-API-Key: $2" -d "$BODY"; echo
echo "--- Consumer 3 (valid) ---"; curl -s -X POST $URL -H "$H" -H "X-API-Key: $3" -d "$BODY"; echo
echo "--- Invalid key ---";        curl -s -X POST $URL -H "$H" -H "X-API-Key: WRONGKEY123" -d "$BODY"; echo
echo "--- Missing key ---";        curl -s -X POST $URL -H "$H" -d "$BODY"; echo
