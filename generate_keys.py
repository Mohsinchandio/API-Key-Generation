"""Generate three unique API keys (one per consumer).

 - The RAW keys are written to issued_keys.txt  -> share each key privately
   with its tester, then delete the file.
 - Only SHA-256 HASHES are written to api_keys.json -> this is what the server
   reads, so a leaked server file does not leak usable keys.

Run:  python generate_keys.py
"""
import hashlib
import json
import secrets

CONSUMERS = ["consumer_alice", "consumer_bob", "consumer_charlie"]

hashed = {}
lines = []
for name in CONSUMERS:
    key = secrets.token_urlsafe(32)              # cryptographically secure
    hashed[hashlib.sha256(key.encode()).hexdigest()] = name
    lines.append(f"{name}: {key}")

with open("api_keys.json", "w") as f:
    json.dump(hashed, f, indent=2)

with open("issued_keys.txt", "w") as f:
    f.write("\n".join(lines) + "\n")

print("Keys generated.")
print("  api_keys.json   -> used by the server (hashes only)")
print("  issued_keys.txt -> raw keys; share privately, then delete this file\n")
print("\n".join(lines))
