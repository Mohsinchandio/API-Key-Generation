# API Key Generation and Sharing – Flask Text-Processing API

RootSoftware develops a text-processing API that other developers need to access. This project is a Flask API protected by **API keys**. Three unique keys are generated, one for each of three API consumers, and every request must send its key in the `X-API-Key` HTTP header.

**Author:** Mohsin – BSCS, SZABIST Larkana

## Features
- `POST /process` accepts JSON `{"text": "..."}` and returns the processed (uppercase) text, plus length and word count
- Three unique API keys, one per consumer, generated with Python's `secrets` module
- The key is read from the `X-API-Key` request header and validated before any processing
- Valid key → `200 OK` with the result
- Invalid or missing key → `401 Unauthorized`
- Only SHA-256 **hashes** of the keys are stored on the server, and keys are compared in constant time (`hmac.compare_digest`)

## Files
| File | Purpose |
|------|---------|
| `app.py` | Flask API with API-key validation |
| `generate_keys.py` | Generates the three keys for the three consumers |
| `test_curl.sh` | cURL test script (Git Bash / Linux / Mac) |
| `requirements.txt` | Python packages |

`api_keys.json` and `issued_keys.txt` are created by `generate_keys.py`. They are **not** in this repository, so real keys are never exposed.

## How to run

**1. Install packages**
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
(If PowerShell blocks activation: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)

**2. Generate the three keys (once)**
```
python generate_keys.py
```
Share each key privately with its tester. Do not publish the keys.

**3. Start the API**
```
python app.py
```
Runs at http://127.0.0.1:5001

## Test with cURL

Valid key (expect `200`):
```
curl -X POST http://127.0.0.1:5001/process -H "Content-Type: application/json" -H "X-API-Key: YOUR_KEY" -d '{"text":"hello rootsoftware"}'
```
Example response:
```
{"consumer":"consumer_alice","length":18,"original":"hello rootsoftware","processed":"HELLO ROOTSOFTWARE","word_count":2}
```

Invalid key (expect `401`):
```
curl -X POST http://127.0.0.1:5001/process -H "Content-Type: application/json" -H "X-API-Key: WRONGKEY" -d '{"text":"hello"}'
```
Response: `{"error":"Invalid API key."}`

Missing key (expect `401`):
```
curl -X POST http://127.0.0.1:5001/process -H "Content-Type: application/json" -d '{"text":"hello"}'
```
Response: `{"error":"Missing API key. Send it in the X-API-Key header."}`

On Windows PowerShell, use `curl.exe`, and put the JSON in a file (`-d "@body.json"`) to avoid quoting problems.

## Security note
Keys are generated with `secrets` for this classroom exercise. Real keys are never committed to this repository or shown in the demo video.

### Watch the Video  Demonstration of the API Key Generation and Sharing
click here to watch the video
https://drive.google.com/file/d/1iM7doThGWNmEAmFvTEawnCmSfwfoo6iQ/view?usp=sharing
