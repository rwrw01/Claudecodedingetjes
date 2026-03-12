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
        "model": "claude-sonnet-4-6-20250514",
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
            if 'titel' in header:
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


def download_image(url: str) -> tuple[bytes, str]:
    """Download een afbeelding en retourneer (bytes, media_type)."""
    req = urllib.request.Request(url, headers={'User-Agent': 'GitHub-Actions-Lesson-Generator'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        content_type = resp.headers.get('Content-Type', 'image/png')

    if 'jpeg' in content_type or 'jpg' in content_type or url.lower().endswith(('.jpg', '.jpeg')):
        media_type = 'image/jpeg'
    elif 'gif' in content_type or url.lower().endswith('.gif'):
        media_type = 'image/gif'
    elif 'webp' in content_type or url.lower().endswith('.webp'):
        media_type = 'image/webp'
    else:
        media_type = 'image/png'

    return data, media_type


def call_deepseek_api(api_key: str, images: list[dict], prompt_text: str, user_context: str) -> str:
    """Roep de DeepSeek API aan (OpenAI-compatibel format)."""
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

    # OpenAI-compatibel antwoord format
    choices = result.get('choices', [])
    if choices:
        return choices[0].get('message', {}).get('content', '')

    print("FOUT: Geen antwoord van DeepSeek API.")
    print(f"  Response: {json.dumps(result, indent=2)[:500]}")
    sys.exit(1)


def call_claude_api(api_key: str, images: list[dict], prompt_text: str, user_context: str) -> str:
    """Roep de Claude API aan (Anthropic format)."""
    config = PROVIDERS["claude"]

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
        "model": config["model"],
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

    for block in result.get('content', []):
        if block.get('type') == 'text':
            return block['text']

    print("FOUT: Geen tekstantwoord van Claude API.")
    sys.exit(1)


def call_ai_api(provider: str, api_key: str, images: list[dict], prompt_text: str, user_context: str) -> str:
    """Roep de juiste AI API aan op basis van de provider."""
    if provider == "deepseek":
        return call_deepseek_api(api_key, images, prompt_text, user_context)
    elif provider == "claude":
        return call_claude_api(api_key, images, prompt_text, user_context)
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


def main():
    # Bepaal provider
    provider = get_provider()
    config = PROVIDERS[provider]
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

    print(f"  Parsed: titel='{titel}', vak='{vak}', niveau='{niveau}', fotos={len(fotos)}, extra={len(extra)} chars")

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
    response = call_ai_api(provider, api_key, images, prompt_text, user_context)
    print(f"  Antwoord ontvangen ({len(response)} karakters)")

    # Extraheer HTML
    html_content = extract_html(response)
    print(f"  HTML geëxtraheerd ({len(html_content)} karakters)")

    # Bepaal de uitvoermap
    vak_slug = slugify(vak) if vak else 'overig'
    niveau_slug = slugify(niveau) if niveau else 'algemeen'
    titel_slug = slugify(titel)
    lesson_dir = Path(issue_author) / vak_slug / f"{niveau_slug}-{titel_slug}"
    output_path = lesson_dir / 'index.html'

    # Maak de map aan en schrijf het bestand
    full_output = Path.cwd() / output_path
    full_output.parent.mkdir(parents=True, exist_ok=True)
    full_output.write_text(html_content, encoding='utf-8')
    print(f"  Les opgeslagen: {output_path}")

    # Schrijf metadata als JSON
    metadata = {
        "issue_number": int(issue_number),
        "issue_author": issue_author,
        "titel": titel,
        "vak": vak,
        "niveau": niveau,
        "fotos_count": len(fotos),
        "generated_path": str(output_path),
        "ai_provider": provider,
        "ai_model": config["model"],
    }
    meta_path = full_output.parent / 'metadata.json'
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')

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
