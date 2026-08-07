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

def _run_models(models messages, max_tokens=160, temperature=0.3):
    last_err = None
    for model in models:
        data, err = query_hf_api({"model":model, "messages":messages, "max_tokens":max_tokens, "temperature":temperature})
        if err:
            last_err = err
            continue
        out = _extract_text(data)
        if out:
            return out, None
        last_err = "No text output from model."
    return None, last_err or "All models failed."

def _words(text:str):
    return re.findall(r"\S+", (text or "").strip())
def _exact_n_words(text: str, n:int) -> str:
    return " ".join(_words(text)[:n])
def _ensure_sentence_end(text: str) -> str:
    t = (text or "").strip()
    if t and t[-1] not in ".!?":
        t += "."
    return t
def generate_text(prompt:str max_tokens: int = 220)-> str:
txt, err = _run_models(TEXT_MODELS, [{"role":"user", "content":prompt}], max_tokens=max_new_tokens, temperature=0.4)
