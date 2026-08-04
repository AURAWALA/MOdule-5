from config import HF_API_KEY
import requests, base64, os, re, time
from PIL import Image
from colorama import init, Fore, Style

init(autoreset=True)

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}

VISION_MODELS = [
    "moonshotai/Kimi-K2.6:novita",
    "meta-llama/Llama-4-Maverick-17b-128E-Instruct:sambanova",
    "meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova",
]
TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mixtral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
]

def _data_url(path:str ) -> str:
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")
    
def query_hf_api(payload:dict):
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS, json=payload, timeout=120)
    except Exception:
        msg = (r.text or "").strip() or r.reason or "Request Failed"
        return None, f"Status {r.status_code}: {msg}"
    try:
        return r.json(), None
    except Exception:
        return None, "Non-JSON response from API."
    
def _extract_text(data) -> str:
    msg = (data or {}).get("choices", [{}])[0].get("message", {}) or {}
    return (msg.get("content" or "")).strip()