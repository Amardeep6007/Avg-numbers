from fastapi import FastAPI
import httpx
import asyncio
from collections import deque
import time

app = FastAPI()

WINDOW_SIZE = 10
window = deque(maxlen=WINDOW_SIZE)

# --- Auth & API Info ---
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQ0MDM1NzgzLCJpYXQiOjE3NDQwMzU0ODMsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6ImQzYzBkMTQyLTQ5YTgtNGQ3Mi1hNTUxLTYyOTc3OGZmMjk0MyIsInN1YiI6ImFrdW1hcjFfbWUyNEB0aGFwYXIuZWR1In0sImVtYWlsIjoiYWt1bWFyMV9tZTI0QHRoYXBhci5lZHUiLCJuYW1lIjoiYW1hcmRlZXAga3VtYXIiLCJyb2xsTm8iOiI4MDI0MzIwMDEzIiwiYWNjZXNzQ29kZSI6IlhyeWVIRCIsImNsaWVudElEIjoiZDNjMGQxNDItNDlhOC00ZDcyLWE1NTEtNjI5Nzc4ZmYyOTQzIiwiY2xpZW50U2VjcmV0IjoiY2ZQeXNCTUFLQXp2Zk1oUSJ9.vGaitafuptqAODajESculR99y-N4ImQAdxmr81dFGvk"

# Use these final URLs from spec after /test/register response
NUMBER_API_URLS = {
    "p": "http://20.244.56.144/primes",
    "f": "http://20.244.56.144/fibo",
    "e": "http://20.244.56.144/even",
    "r": "http://20.244.56.144/rand"
}


# --- Core Logic ---
async def fetch_numbers(number_id: str):
    url = NUMBER_API_URLS.get(number_id)
    if not url:
        return []

    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    try:
        async with httpx.AsyncClient(timeout=0.5) as client:
            response = await client.get(url, headers=headers)
            print(f"STATUS: {response.status_code}")
            print(f"RESPONSE: {response.text}")

            if response.status_code == 200:
                return response.json().get("numbers", [])
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
        return []

    return []


@app.get("/numbers/{number_id}")
async def get_numbers(number_id: str):
    start = time.time()

    if number_id not in NUMBER_API_URLS:
        return {"error": "Invalid ID. Use 'p', 'f', 'e', or 'r'."}

    prev_window = list(window)
    new_numbers = await fetch_numbers(number_id)

    for num in new_numbers:
        if num not in window:
            window.append(num)

    curr_window = list(window)
    avg = sum(curr_window) / len(curr_window) if curr_window else 0

    end = time.time()
    if (end - start) > 0.5:
        print("⚠️ Took longer than 500ms")

    return {
        "windowPrevState": prev_window,
        "windowCurrState": curr_window,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }
