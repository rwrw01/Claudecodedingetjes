#!/usr/bin/env python3
"""
Automatische lesgeneratie vanuit GitHub Issues.

Dit script:
1. Leest een GitHub Issue met foto's en metadata
2. Stuurt de foto's naar DeepSeek of Claude API met een lesgeneratie-prompt
3. Slaat de gegenereerde les op in de juiste map
4. Update het issue met de resultaten

Ondersteunde providers:
- claude (standaard) — ondersteunt afbeeldingen, hogere kwaliteit
- deepseek — goedkoop, alleen tekst (geen afbeeldingen)
"""

import io
import os
import re
import sys
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path


# Provider configuratie
PROVIDERS = {
    "deepseek": {
        "name": "DeepSeek",
        "api_url": "https://api.deepseek.com/chat/completions",
        "model": "deepseek-chat",
        "max_tokens": 16000,
        "env_key": "DEEPSEEK_API_KEY",
    },
    "claude": {
        "name": "Claude",
        "api_url": "https://api.anthropic.com/v1/messages",
        "model": "auto",  # Wordt automatisch bepaald via /v1/models
        "model_preference": ["claude-sonnet"],  # Voorkeur: nieuwste Sonnet
        "max_tokens": 16000,
        "env_key": "ANTHROPIC_API_KEY",
    },
}


def get_env(name: str, required: bool = True) -> str:
    """Haal een environment variable op."""
    value = os.environ.get(name, "").strip()
    if not value and required:
        print(f"FOUT: Environment variable {name} is niet gezet.")
        sys.exit(1)
    return value


def get_provider() -> str:
    """Bepaal welke AI-provider te gebruiken. Standaard: claude (ondersteunt afbeeldingen)."""
    provider = os.environ.get("AI_PROVIDER", "claude").strip().lower()
    if provider not in PROVIDERS:
        print(f"WAARSCHUWING: Onbekende provider '{provider}', gebruik deepseek.")
        provider = "deepseek"
    return provider


def resolve_claude_model(api_key: str) -> str:
    """Vraag de Anthropic /v1/models API op en kies het nieuwste Sonnet model."""
    try:
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/models?limit=50",
            headers={
                'x-api-key': api_key,
                'anthropic-version': '2023-06-01',
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        models = result.get('data', [])
        # Filter op sonnet modellen, sorteer op created_at (nieuwste eerst)
        sonnet_models = [
            m for m in models
            if 'sonnet' in m.get('id', '').lower()
        ]
        sonnet_models.sort(key=lambda m: m.get('created_at', ''), reverse=True)

        if sonnet_models:
            model_id = sonnet_models[0]['id']
            print(f"  Automatisch gekozen model: {model_id} (nieuwste Sonnet)")
            return model_id

        # Fallback: neem het eerste beschikbare model
        if models:
            model_id = models[0]['id']
            print(f"  Geen Sonnet gevonden, gebruik: {model_id}")
            return model_id

    except Exception as e:
        print(f"  WAARSCHUWING: Kon modellen niet ophalen ({e})")

    # Hardcoded fallback
    fallback = "claude-sonnet-4-5-20250929"
    print(f"  Gebruik fallback model: {fallback}")
    return fallback


def slugify(text: str) -> str:
    """Maak een URL-veilige slug van een tekst."""
    text = text.lower().strip()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def parse_issue_body(body: str) -> dict:
    """Parse de gestructureerde issue body (GitHub issue form format)."""
    result = {
        "naam": "",
        "titel": "",
        "vak": "",
        "vak_anders": "",
        "niveau": "",
        "fotos": [],
        "extra": "",
    }

    current_field = None
    current_value_lines = []

    lines = body.split('\n')
    for line in lines:
        if line.startswith('### '):
            if current_field:
                result[current_field] = '\n'.join(current_value_lines).strip()
            header = line[4:].strip().lower()
            if 'naam' in header and 'je naam' in header:
                current_field = 'naam'
            elif 'titel' in header:
                current_field = 'titel'
            elif 'vak' in header and 'ander' in header:
                current_field = 'vak_anders'
            elif 'vak' in header:
                current_field = 'vak'
            elif 'niveau' in header:
                current_field = 'niveau'
            elif "foto" in header:
                current_field = 'fotos_raw'
            elif 'extra' in header or 'instructie' in header:
                current_field = 'extra'
            else:
                current_field = None
            current_value_lines = []
        elif current_field:
            current_value_lines.append(line)

    if current_field:
        result[current_field] = '\n'.join(current_value_lines).strip()

    # Parse foto URLs — ondersteunt diverse GitHub image hosting domeinen
    foto_text = result.get('fotos_raw', '') or body
    foto_urls = re.findall(
        r'https://(?:user-images\.githubusercontent\.com|private-user-images\.githubusercontent\.com|github\.user-content\.com|github\.com/user-attachments|github\.com)[^\s\)\"\']+\.(?:png|jpg|jpeg|gif|webp)',
        foto_text,
        re.IGNORECASE,
    )
    # Markdown afbeeldingen: ![alt](url)
    foto_urls += re.findall(
        r'!\[.*?\]\((https://[^\s\)]+)\)',
        foto_text,
    )
    # GitHub attachment URLs zonder extensie (bijv. github.com/user-attachments/assets/...)
    foto_urls += re.findall(
        r'https://github\.com/user-attachments/assets/[^\s\)\"\']+',
        foto_text,
    )
    seen = set()
    unique_urls = []
    for url in foto_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    result['fotos'] = unique_urls

    if result.get('vak', '').lower() == 'anders' and result.get('vak_anders'):
        result['vak'] = result['vak_anders']

    result.pop('fotos_raw', None)
    result.pop('vak_anders', None)

    return result


def resize_image(data: bytes, max_bytes: int = 3_500_000, max_dim: int = 2048) -> tuple[bytes, str]:
    """Verklein een afbeelding zodat deze binnen de API-limieten past.

    Retourneert (bytes, media_type). Altijd JPEG output voor compressie.
    Claude API max: ~5MB per afbeelding, we mikken op 3.5MB voor marge.
    """
    try:
        from PIL import Image
    except ImportError:
        # Pillow niet beschikbaar — geef origineel terug en hoop op het beste
        print("  WAARSCHUWING: Pillow niet geïnstalleerd, afbeelding niet verkleind")
        return data, 'image/jpeg'

    img = Image.open(io.BytesIO(data))

    # Converteer naar RGB als nodig (bijv. RGBA, palette)
    if img.mode not in ('RGB', 'L'):
        img = img.convert('RGB')

    # Verklein als de dimensies te groot zijn
    w, h = img.size
    if w > max_dim or h > max_dim:
        ratio = min(max_dim / w, max_dim / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        print(f"  Verkleind van {w}x{h} naar {new_w}x{new_h}")

    # Probeer met afnemende kwaliteit tot het past
    for quality in (85, 70, 55, 40):
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=quality, optimize=True)
        result = buf.getvalue()
        if len(result) <= max_bytes:
            print(f"  JPEG kwaliteit {quality}: {len(result) // 1024}KB")
            return result, 'image/jpeg'

    # Als het nog steeds te groot is, verklein verder
    for scale in (0.75, 0.5, 0.35):
        w, h = img.size
        img_small = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        buf = io.BytesIO()
        img_small.save(buf, format='JPEG', quality=50, optimize=True)
        result = buf.getvalue()
        if len(result) <= max_bytes:
            print(f"  Verder verkleind ({scale}x): {len(result) // 1024}KB")
            return result, 'image/jpeg'

    print(f"  WAARSCHUWING: afbeelding nog steeds {len(result) // 1024}KB na maximale compressie")
    return result, 'image/jpeg'


def download_image(url: str) -> tuple[bytes, str]:
    """Download een afbeelding, verklein indien nodig, en retourneer (bytes, media_type)."""
    req = urllib.request.Request(url, headers={'User-Agent': 'GitHub-Actions-Lesson-Generator'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()

    original_kb = len(data) // 1024
    print(f"  Origineel: {original_kb}KB")

    # Verklein als groter dan 3.5MB (Claude API limiet ~5MB per afbeelding)
    if len(data) > 3_500_000:
        data, media_type = resize_image(data)
    else:
        # Bepaal media type
        if url.lower().endswith(('.jpg', '.jpeg')) or data[:3] == b'\xff\xd8\xff':
            media_type = 'image/jpeg'
        elif url.lower().endswith('.png') or data[:4] == b'\x89PNG':
            media_type = 'image/png'
        elif url.lower().endswith('.gif') or data[:3] == b'GIF':
            media_type = 'image/gif'
        elif url.lower().endswith('.webp') or data[8:12] == b'WEBP':
            media_type = 'image/webp'
        else:
            # Onbekend format — converteer naar JPEG voor veiligheid
            data, media_type = resize_image(data)

    return data, media_type


def call_deepseek_api(api_key: str, images: list[dict], prompt_text: str, user_context: str) -> tuple[str, dict]:
    """Roep de DeepSeek API aan (OpenAI-compatibel format). Retourneert (tekst, usage)."""
    config = PROVIDERS["deepseek"]

    # Bouw de content array op (OpenAI vision format)
    content = []

    for img in images:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:{img['media_type']};base64,{img['data_b64']}",
            },
        })

    content.append({
        "type": "text",
        "text": user_context,
    })

    payload = {
        "model": config["model"],
        "max_tokens": config["max_tokens"],
        "messages": [
            {
                "role": "system",
                "content": prompt_text,
            },
            {
                "role": "user",
                "content": content,
            },
        ],
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        config["api_url"],
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else 'Geen details'
        print(f"DeepSeek API fout ({e.code}): {error_body}")
        sys.exit(1)

    usage = log_usage(result, "deepseek", config["model"])

    # OpenAI-compatibel antwoord format
    choices = result.get('choices', [])
    if choices:
        return choices[0].get('message', {}).get('content', ''), usage

    print("FOUT: Geen antwoord van DeepSeek API.")
    print(f"  Response: {json.dumps(result, indent=2)[:500]}")
    sys.exit(1)


def call_claude_api(api_key: str, images: list[dict], prompt_text: str, user_context: str, model: str = "") -> tuple[str, dict]:
    """Roep de Claude API aan (Anthropic format). Retourneert (tekst, usage)."""
    config = PROVIDERS["claude"]
    model = model or config["model"]

    content = []
    for img in images:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": img["media_type"],
                "data": img["data_b64"],
            },
        })

    content.append({
        "type": "text",
        "text": user_context,
    })

    payload = {
        "model": model,
        "max_tokens": config["max_tokens"],
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
        "system": prompt_text,
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        config["api_url"],
        data=data,
        headers={
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01',
        },
        method='POST',
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else 'Geen details'
        print(f"Claude API fout ({e.code}): {error_body}")
        sys.exit(1)

    usage = log_usage(result, "claude", model)

    for block in result.get('content', []):
        if block.get('type') == 'text':
            return block['text'], usage

    print("FOUT: Geen tekstantwoord van Claude API.")
    sys.exit(1)


# Prijzen per 1M tokens (USD) — bijwerken als prijzen veranderen
PRICING = {
    "claude-sonnet": {"input": 3.00, "output": 15.00},   # Sonnet 4.x
    "claude-opus": {"input": 15.00, "output": 75.00},     # Opus 4.x
    "claude-haiku": {"input": 0.80, "output": 4.00},      # Haiku
    "deepseek-chat": {"input": 0.28, "output": 0.42},      # DeepSeek V3.2 (cache miss)
    "deepseek-reasoner": {"input": 0.28, "output": 0.42}, # DeepSeek V3.2 reasoner
}


def log_usage(result: dict, provider: str, model: str) -> dict:
    """Log token-gebruik en geschatte kosten. Retourneert usage-dict voor metadata."""
    usage = result.get('usage', {})
    if not usage:
        return {}

    if provider == "claude":
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        cache_read = usage.get('cache_read_input_tokens', 0)
    else:
        # OpenAI-compatibel (DeepSeek)
        input_tokens = usage.get('prompt_tokens', 0)
        output_tokens = usage.get('completion_tokens', 0)
        cache_read = 0

    total_tokens = input_tokens + output_tokens

    # Zoek prijzen op basis van model naam
    pricing = None
    for key, prices in PRICING.items():
        if key in model:
            pricing = prices
            break

    if pricing:
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        total_cost = input_cost + output_cost

        print(f"\n  === Token-gebruik ===")
        print(f"  Input tokens:  {input_tokens:>8,}")
        if cache_read:
            print(f"  Cache read:    {cache_read:>8,}")
        print(f"  Output tokens: {output_tokens:>8,}")
        print(f"  Totaal tokens: {total_tokens:>8,}")
        print(f"  ---")
        print(f"  Input kosten:  ${input_cost:.4f}")
        print(f"  Output kosten: ${output_cost:.4f}")
        print(f"  Totaal kosten: ${total_cost:.4f} (~€{total_cost * 0.92:.4f})")
        print(f"  ===================\n")
    else:
        print(f"\n  Tokens: {input_tokens} input + {output_tokens} output = {total_tokens} totaal")
        print(f"  (Prijzen onbekend voor model {model})\n")
        total_cost = None

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cache_read_tokens": cache_read,
        "estimated_cost_usd": round(total_cost, 4) if total_cost else None,
    }


def call_ai_api(provider: str, api_key: str, images: list[dict], prompt_text: str, user_context: str, model: str = "") -> tuple[str, dict]:
    """Roep de juiste AI API aan op basis van de provider. Retourneert (tekst, usage)."""
    if provider == "deepseek":
        return call_deepseek_api(api_key, images, prompt_text, user_context)
    elif provider == "claude":
        return call_claude_api(api_key, images, prompt_text, user_context, model)
    else:
        print(f"FOUT: Onbekende provider '{provider}'")
        sys.exit(1)


def extract_html(response: str) -> str:
    """Extraheer het HTML-bestand uit het API-antwoord."""
    match = re.search(r'```html?\s*\n(.*?)```', response, re.DOTALL)
    if match:
        return match.group(1).strip()

    match = re.search(r'(<!DOCTYPE html>.*</html>)', response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    if '<html' in response.lower() and '</html>' in response.lower():
        return response.strip()

    print("WAARSCHUWING: Kon geen HTML extraheren uit het antwoord.")
    return response


# Vak-kleuren (zelfde als index.html)
VAK_KLEUREN = {
    'wiskunde':       {'color': '#2563eb', 'bg': '#dbeafe', 'gradient': '#1e3a5f,#2563eb', 'icon': 'Wi'},
    'scheikunde':     {'color': '#059669', 'bg': '#d1fae5', 'gradient': '#064e3b,#059669', 'icon': 'Sk'},
    'biologie':       {'color': '#16a34a', 'bg': '#dcfce7', 'gradient': '#14532d,#16a34a', 'icon': 'Bi'},
    'natuurkunde':    {'color': '#7c3aed', 'bg': '#ede9fe', 'gradient': '#4c1d95,#7c3aed', 'icon': 'Na'},
    'maatschappijleer': {'color': '#dc2626', 'bg': '#fee2e2', 'gradient': '#7f1d1d,#dc2626', 'icon': 'Ma'},
    'geschiedenis':   {'color': '#b45309', 'bg': '#fef3c7', 'gradient': '#78350f,#b45309', 'icon': 'Gs'},
    'aardrijkskunde': {'color': '#0891b2', 'bg': '#cffafe', 'gradient': '#164e63,#0891b2', 'icon': 'Ak'},
    'economie':       {'color': '#4f46e5', 'bg': '#e0e7ff', 'gradient': '#312e81,#4f46e5', 'icon': 'Ec'},
    'nederlands':     {'color': '#e11d48', 'bg': '#ffe4e6', 'gradient': '#881337,#e11d48', 'icon': 'Ne'},
    'engels':         {'color': '#0284c7', 'bg': '#e0f2fe', 'gradient': '#0c4a6e,#0284c7', 'icon': 'En'},
}
VAK_DEFAULT = {'color': '#6366f1', 'bg': '#e0e7ff', 'gradient': '#3730a3,#6366f1', 'icon': '?'}

HOME_URL = "https://rwrw01.github.io/Claudecodedingetjes/"


def _index_template(title: str, breadcrumb_html: str, cards_html: str) -> str:
    """Genereer een index-pagina HTML."""
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Interactieve lesstof</title>
    <style>
        :root {{ --bg:#f8fafc; --card:#ffffff; --text:#1e293b; --muted:#64748b; --border:#e2e8f0; --radius:12px; }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family:'Segoe UI',system-ui,-apple-system,sans-serif; background:var(--bg); color:var(--text); line-height:1.6; min-height:100vh; display:flex; flex-direction:column; }}
        header {{ background:linear-gradient(135deg,#1e293b,#334155); color:white; padding:2.5rem 1rem; text-align:center; }}
        header h1 {{ font-size:2rem; margin-bottom:0.3rem; }}
        header p {{ opacity:0.8; font-size:1rem; }}
        .breadcrumb {{ padding:1rem; max-width:700px; margin:0 auto; font-size:0.9rem; color:var(--muted); }}
        .breadcrumb a {{ color:#2563eb; text-decoration:none; }}
        .breadcrumb a:hover {{ text-decoration:underline; }}
        .container {{ max-width:700px; margin:0 auto; padding:1rem 1rem 2.5rem; flex:1; }}
        .card {{ display:flex; align-items:center; gap:1.25rem; background:var(--card); border:1px solid var(--border); border-radius:var(--radius); box-shadow:0 1px 3px rgba(0,0,0,0.08); padding:1.5rem; margin-bottom:1.25rem; text-decoration:none; color:var(--text); transition:transform 0.15s,box-shadow 0.15s; }}
        .card:hover {{ transform:translateY(-2px); box-shadow:0 6px 16px rgba(0,0,0,0.1); }}
        .card-icon {{ width:56px; height:56px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.3rem; color:white; flex-shrink:0; }}
        .card h2 {{ font-size:1.2rem; margin-bottom:0.2rem; }}
        .card p {{ color:var(--muted); font-size:0.9rem; margin:0; }}
        .badge {{ font-size:0.75rem; font-weight:600; padding:0.15rem 0.5rem; border-radius:999px; display:inline-block; margin-top:0.4rem; }}
        footer {{ text-align:center; padding:2rem 1rem; color:var(--muted); font-size:0.85rem; }}
    </style>
</head>
<body>
<header>
    <h1>{title}</h1>
    <p>Interactieve lesstof</p>
</header>
<nav class="breadcrumb">{breadcrumb_html}</nav>
<div class="container">
{cards_html}
</div>
<footer>
    <p>Interactieve lesstof</p>
    <p style="margin-top:0.75rem;font-size:0.8rem;">
        Gemaakt door <strong>Ralph Wagter</strong> met <a href="https://claude.ai/code" style="color:#2563eb;">Claude Code</a>.
        Vrij hergebruik onder <a href="https://eupl.eu/" style="color:#2563eb;">EUPL-1.2</a>.
        <a href="https://github.com/rwrw01/Claudecodedingetjes" style="color:#2563eb;">GitHub</a>
    </p>
</footer>
</body>
</html>"""


def _card_html(href: str, title: str, subtitle: str, vak_slug: str = "", badge: str = "") -> str:
    """Genereer een enkele kaart."""
    cfg = VAK_KLEUREN.get(vak_slug, VAK_DEFAULT)
    icon = cfg['icon']
    badge_html = f'<span class="badge" style="background:{cfg["bg"]};color:{cfg["color"]};">{badge}</span>' if badge else ''
    return f"""    <a href="{href}" class="card">
        <div class="card-icon" style="background:linear-gradient(135deg,{cfg['gradient']});">{icon}</div>
        <div>
            <h2 style="color:{cfg['color']};">{title}</h2>
            <p>{subtitle}</p>
            {badge_html}
        </div>
    </a>"""


def get_display_name(author_dir: Path, author: str) -> str:
    """Lees de friendly name uit profile.json, of gebruik de GitHub username."""
    profile_path = author_dir / 'profile.json'
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding='utf-8'))
            return profile.get('display_name', author)
        except Exception:
            pass
    return author


def save_display_name(author_dir: Path, author: str, name: str):
    """Sla de friendly name op in profile.json (update alleen als naam niet leeg is)."""
    profile_path = author_dir / 'profile.json'
    profile = {}
    if profile_path.exists():
        try:
            profile = json.loads(profile_path.read_text(encoding='utf-8'))
        except Exception:
            pass
    if name:
        profile['display_name'] = name
        profile['github_username'] = author
        profile_path.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding='utf-8')


def generate_index_pages(author: str):
    """Genereer index-pagina's op elk niveau: user/ user/vak/ user/vak/niveau/"""
    author_dir = Path.cwd() / author
    if not author_dir.is_dir():
        return

    display_name = get_display_name(author_dir, author)
    print(f"Index-pagina's genereren voor {display_name} ({author})...")

    # Niveau 1: user/index.html — overzicht van vakken
    vak_dirs = sorted([d for d in author_dir.iterdir() if d.is_dir()])
    cards = []
    for vak_dir in vak_dirs:
        vak_name = vak_dir.name
        lesson_count = sum(1 for _ in vak_dir.rglob('metadata.json'))
        pretty_name = vak_name.replace('-', ' ').title()
        cards.append(_card_html(
            href=f"{vak_name}/",
            title=pretty_name,
            subtitle=f"{lesson_count} {'les' if lesson_count == 1 else 'lessen'}",
            vak_slug=vak_name,
            badge=f"{lesson_count} {'les' if lesson_count == 1 else 'lessen'}",
        ))

    breadcrumb = f'<a href="{HOME_URL}">Home</a> &rsaquo; {display_name}'
    index_path = author_dir / 'index.html'
    index_path.write_text(
        _index_template(f"Lessen van {display_name}", breadcrumb, '\n'.join(cards)),
        encoding='utf-8',
    )
    print(f"  {index_path.relative_to(Path.cwd())}")

    # Niveau 2: user/vak/index.html — overzicht van niveaus
    for vak_dir in vak_dirs:
        vak_name = vak_dir.name
        pretty_vak = vak_name.replace('-', ' ').title()
        niveau_dirs = sorted([d for d in vak_dir.iterdir() if d.is_dir()])
        cards = []
        for niveau_dir in niveau_dirs:
            niveau_name = niveau_dir.name
            lesson_count = sum(1 for _ in niveau_dir.rglob('metadata.json'))
            pretty_niveau = niveau_name.replace('-', ' ').upper()
            cards.append(_card_html(
                href=f"{niveau_name}/",
                title=pretty_niveau,
                subtitle=f"{lesson_count} {'les' if lesson_count == 1 else 'lessen'}",
                vak_slug=vak_name,
                badge=f"{lesson_count} {'les' if lesson_count == 1 else 'lessen'}",
            ))

        breadcrumb = f'<a href="{HOME_URL}">Home</a> &rsaquo; <a href="../">{display_name}</a> &rsaquo; {pretty_vak}'
        index_path = vak_dir / 'index.html'
        index_path.write_text(
            _index_template(f"{pretty_vak} — {display_name}", breadcrumb, '\n'.join(cards)),
            encoding='utf-8',
        )
        print(f"  {index_path.relative_to(Path.cwd())}")

        # Niveau 3: user/vak/niveau/index.html — overzicht van lessen
        for niveau_dir in niveau_dirs:
            niveau_name = niveau_dir.name
            pretty_niveau = niveau_name.replace('-', ' ').upper()
            lesson_dirs = sorted([d for d in niveau_dir.iterdir() if d.is_dir()])
            cards = []
            for les_dir in lesson_dirs:
                meta_file = les_dir / 'metadata.json'
                if meta_file.exists():
                    meta = json.loads(meta_file.read_text(encoding='utf-8'))
                    titel = meta.get('titel', les_dir.name.replace('-', ' ').title())
                    subtitle = f"Issue #{meta.get('issue_number', '?')}"
                else:
                    titel = les_dir.name.replace('-', ' ').title()
                    subtitle = ""
                cards.append(_card_html(
                    href=f"{les_dir.name}/",
                    title=titel,
                    subtitle=subtitle,
                    vak_slug=vak_name,
                ))

            breadcrumb = (
                f'<a href="{HOME_URL}">Home</a> &rsaquo; '
                f'<a href="../../">{display_name}</a> &rsaquo; '
                f'<a href="../">{pretty_vak}</a> &rsaquo; {pretty_niveau}'
            )
            index_path = niveau_dir / 'index.html'
            index_path.write_text(
                _index_template(f"{pretty_vak} {pretty_niveau} — {display_name}", breadcrumb, '\n'.join(cards)),
                encoding='utf-8',
            )
            print(f"  {index_path.relative_to(Path.cwd())}")

    print("  Index-pagina's klaar.")


def main():
    # Bepaal provider
    provider = get_provider()
    config = PROVIDERS[provider].copy()

    # Voor Claude: bepaal automatisch het nieuwste model
    if provider == "claude" and config["model"] == "auto":
        api_key = get_env(config["env_key"])
        config["model"] = resolve_claude_model(api_key)

    print(f"AI Provider: {config['name']} ({config['model']})")

    # Haal de API key op voor de gekozen provider
    api_key = get_env(config["env_key"])

    # Overige environment variables
    github_token = get_env('GITHUB_TOKEN')
    repo = get_env('GITHUB_REPOSITORY')
    issue_number = get_env('ISSUE_NUMBER')
    issue_author = get_env('ISSUE_AUTHOR')

    # Issue body: lees uit bestand (veiliger dan env var bij multiline content)
    issue_body_file = os.environ.get('ISSUE_BODY_FILE', '').strip()
    if issue_body_file and Path(issue_body_file).exists():
        issue_body = Path(issue_body_file).read_text(encoding='utf-8')
        print(f"  Issue body gelezen uit bestand: {issue_body_file} ({len(issue_body)} chars)")
    else:
        issue_body = get_env('ISSUE_BODY')
        print(f"  Issue body gelezen uit env var ({len(issue_body)} chars)")

    print(f"Verwerk issue #{issue_number} van {issue_author}...")
    print(f"  Issue body (eerste 500 chars): {issue_body[:500]}")

    # Parse issue
    parsed = parse_issue_body(issue_body)
    titel = parsed['titel']
    vak = parsed['vak']
    niveau = parsed['niveau']
    fotos = parsed['fotos']
    extra = parsed['extra']
    friendly_name = parsed.get('naam', '').strip()

    print(f"  Parsed: titel='{titel}', vak='{vak}', niveau='{niveau}', fotos={len(fotos)}, naam='{friendly_name}'")

    if not titel:
        print("FOUT: Geen titel gevonden in het issue.")
        sys.exit(1)
    if not fotos:
        print("FOUT: Geen foto's gevonden in het issue.")
        print(f"  Volledige issue body:\n{issue_body}")
        sys.exit(1)

    print(f"  Titel: {titel}")
    print(f"  Vak: {vak}")
    print(f"  Niveau: {niveau}")
    print(f"  Foto's: {len(fotos)} gevonden")

    # Download foto's
    print("Foto's downloaden...")
    images = []
    for i, url in enumerate(fotos):
        print(f"  [{i+1}/{len(fotos)}] {url[:80]}...")
        img_data, media_type = download_image(url)
        images.append({
            "data_b64": base64.b64encode(img_data).decode('utf-8'),
            "media_type": media_type,
        })
    print(f"  {len(images)} foto's gedownload.")

    # Lees de prompt template
    script_dir = Path(__file__).parent
    prompt_path = script_dir / 'lesson-prompt.txt'
    prompt_text = prompt_path.read_text(encoding='utf-8')

    # Bouw de gebruikerscontext op
    user_context = f"""Maak een interactieve les met de volgende gegevens:

- Titel: {titel}
- Vak: {vak}
- Niveau: {niveau}
- Auteur (GitHub): {issue_author}

Analyseer de bijgevoegde foto('s) en maak er een complete interactieve les van.
Onthoud: maak EIGEN voorbeelden, kopieer niet letterlijk.
"""
    if extra:
        user_context += f"\nExtra instructies van de aanvrager:\n{extra}\n"

    # Roep AI API aan
    print(f"{config['name']} API aanroepen...")
    response, usage = call_ai_api(provider, api_key, images, prompt_text, user_context, config["model"])
    print(f"  Antwoord ontvangen ({len(response)} karakters)")

    # Extraheer HTML
    html_content = extract_html(response)
    print(f"  HTML geëxtraheerd ({len(html_content)} karakters)")

    # Bepaal de uitvoermap: user/vak/niveau/hoofdstuk/
    vak_slug = slugify(vak) if vak else 'overig'
    niveau_slug = slugify(niveau) if niveau else 'algemeen'
    titel_slug = slugify(titel)
    lesson_dir = Path(issue_author) / vak_slug / niveau_slug / titel_slug
    output_path = lesson_dir / 'index.html'

    # Maak de map aan en schrijf het bestand
    full_output = Path.cwd() / output_path
    full_output.parent.mkdir(parents=True, exist_ok=True)
    full_output.write_text(html_content, encoding='utf-8')
    print(f"  Les opgeslagen: {output_path}")

    # Sla friendly name op in profile.json (als opgegeven)
    author_dir = Path.cwd() / issue_author
    if friendly_name:
        save_display_name(author_dir, issue_author, friendly_name)
        print(f"  Friendly name opgeslagen: {friendly_name}")

    # Schrijf metadata als JSON
    metadata = {
        "issue_number": int(issue_number),
        "issue_author": issue_author,
        "display_name": friendly_name or get_display_name(author_dir, issue_author),
        "titel": titel,
        "vak": vak,
        "niveau": niveau,
        "fotos_count": len(fotos),
        "generated_path": str(output_path),
        "ai_provider": provider,
        "ai_model": config["model"],
        "usage": usage,
    }
    meta_path = full_output.parent / 'metadata.json'
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')

    # Genereer index-pagina's op elk niveau
    generate_index_pages(issue_author)

    # Output voor GitHub Actions
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"lesson_path={output_path}\n")
            f.write(f"lesson_dir={lesson_dir}\n")
            f.write(f"ai_provider={config['name']}\n")

    print("Klaar!")


if __name__ == '__main__':
    main()
