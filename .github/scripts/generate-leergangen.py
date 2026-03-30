#!/usr/bin/env python3
"""
Genereert indexpagina's voor de leergangen-sectie en een JSON-zoekindex.

Structuur:
  leergangen/index.html              — overzicht alle domeinen
  leergangen/{domein}/index.html     — overzicht leergangen in domein
  leergangen/{domein}/{leergang}/index.html — lessen in leergang
  leergangen/search-index.json       — zoekindex voor client-side search
"""

import json
import yaml
from pathlib import Path

HOME_URL = "https://rwrw01.github.io/Claudecodedingetjes"


def lees_metadata(les_dir: Path) -> dict:
    meta_file = les_dir / 'metadata.json'
    if meta_file.exists():
        return json.loads(meta_file.read_text(encoding='utf-8'))
    return {}


def genereer_domein_index(domein: dict, base_path: Path):
    domein_slug = domein['slug']
    domein_pad = base_path / domein_slug
    domein_pad.mkdir(parents=True, exist_ok=True)

    kaarten = []
    for lg in domein['leergangen']:
        lg_slug = lg['slug']
        kaarten.append(f"""
        <a class="card" href="{lg_slug}/">
            <h3>{lg['naam']}</h3>
            <p class="muted">{lg.get('omschrijving', '')}</p>
        </a>""")

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{domein['naam']} — Leergangen</title>
    {_style()}
</head>
<body>
    <header style="background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:2.5rem 1rem;text-align:center;">
        <h1>{domein['naam']}</h1>
        <p style="opacity:.8">Leergangen</p>
    </header>
    <nav class="breadcrumb">
        <a href="{HOME_URL}">Home</a> &rsaquo;
        <a href="../">Leergangen</a> &rsaquo;
        {domein['naam']}
    </nav>
    <div class="container">
        {''.join(kaarten)}
    </div>
    {_footer()}
</body>
</html>"""
    (domein_pad / 'index.html').write_text(html, encoding='utf-8')
    print(f"  {domein_pad}/index.html")


def genereer_leergang_index(domein: dict, leergang: dict, base_path: Path):
    domein_slug = domein['slug']
    lg_slug = leergang['slug']
    lg_pad = base_path / domein_slug / lg_slug
    lg_pad.mkdir(parents=True, exist_ok=True)

    les_dirs = sorted(
        [d for d in lg_pad.iterdir() if d.is_dir() and (d / 'index.html').exists()],
        key=lambda d: (lees_metadata(d).get('titel', d.name) or d.name).lower()
    ) if lg_pad.exists() else []

    kaarten = []
    for les_dir in les_dirs:
        meta = lees_metadata(les_dir)
        titel = meta.get('titel', les_dir.name.replace('-', ' ').title())
        auteur = meta.get('display_name') or meta.get('friendly_name') or meta.get('issue_author', '')
        kaarten.append(f"""
        <a class="card" href="{les_dir.name}/">
            <h3>{titel}</h3>
            {f'<p class="muted">door {auteur}</p>' if auteur else ''}
        </a>""")

    if not kaarten:
        kaarten = ['<p class="muted">Nog geen lessen in deze leergang.</p>']

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{leergang['naam']} — {domein['naam']}</title>
    {_style()}
</head>
<body>
    <header style="background:linear-gradient(135deg,#3730a3,#6366f1);color:white;padding:2.5rem 1rem;text-align:center;">
        <h1>{leergang['naam']}</h1>
        <p style="opacity:.8">{leergang.get('omschrijving', '')}</p>
    </header>
    <nav class="breadcrumb">
        <a href="{HOME_URL}">Home</a> &rsaquo;
        <a href="../../">Leergangen</a> &rsaquo;
        <a href="../">{domein['naam']}</a> &rsaquo;
        {leergang['naam']}
    </nav>
    <div class="container">
        <div class="search-box">
            <input type="text" id="zoek" placeholder="Zoek in deze leergang..." oninput="zoek(this.value)">
        </div>
        <div id="lessen">{''.join(kaarten)}</div>
    </div>
    {_footer()}
    <script>
    function zoek(q) {{
        q = q.toLowerCase();
        document.querySelectorAll('#lessen .card').forEach(card => {{
            card.style.display = card.textContent.toLowerCase().includes(q) ? '' : 'none';
        }});
    }}
    </script>
</body>
</html>"""
    (lg_pad / 'index.html').write_text(html, encoding='utf-8')
    print(f"  {lg_pad}/index.html")


def genereer_hoofdindex(config: dict, base_path: Path):
    domein_kaarten = []
    for domein in config['domeinen']:
        n_leergangen = len(domein['leergangen'])
        domein_kaarten.append(f"""
        <a class="card" href="{domein['slug']}/">
            <h3>{domein['naam']}</h3>
            <p class="muted">{n_leergangen} leergang{'en' if n_leergangen != 1 else ''}</p>
        </a>""")

    html = f"""<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leergangen — Volwasseneneducatie</title>
    {_style()}
</head>
<body>
    <header style="background:linear-gradient(135deg,#1e293b,#334155);color:white;padding:3rem 1rem;text-align:center;">
        <h1>Leergangen</h1>
        <p style="opacity:.8">Interactieve lessen voor volwasseneneducatie</p>
    </header>
    <nav class="breadcrumb">
        <a href="{HOME_URL}">Home</a> &rsaquo; Leergangen
    </nav>
    <div class="container">
        <div class="search-box">
            <input type="text" id="zoek" placeholder="Zoek door alle leergangen..." oninput="zoekGlobaal(this.value)">
        </div>
        <div id="resultaten" style="display:none"></div>
        <div id="domeinen">{''.join(domein_kaarten)}</div>
    </div>
    {_footer()}
    <script>
    let searchIndex = null;
    async function laadIndex() {{
        try {{
            const r = await fetch('search-index.json');
            searchIndex = await r.json();
        }} catch(e) {{ searchIndex = []; }}
    }}
    laadIndex();
    function zoekGlobaal(q) {{
        if (!q) {{ document.getElementById('domeinen').style.display=''; document.getElementById('resultaten').style.display='none'; return; }}
        document.getElementById('domeinen').style.display='none';
        const res = document.getElementById('resultaten');
        res.style.display='';
        if (!searchIndex) {{ res.innerHTML='<p>Zoekindex laden...</p>'; return; }}
        const hits = searchIndex.filter(l => (l.titel+' '+l.leergang+' '+l.domein+' '+(l.omschrijving||'')).toLowerCase().includes(q.toLowerCase()));
        res.innerHTML = hits.length
            ? hits.map(h => `<a class="card" href="${{HOME_URL}}/${{h.pad}}"><h3>${{h.titel}}</h3><p class="muted">${{h.domein}} &rsaquo; ${{h.leergang}}</p></a>`).join('')
            : '<p class="muted">Geen resultaten gevonden.</p>';
    }}
    </script>
</body>
</html>"""
    (base_path / 'index.html').write_text(html, encoding='utf-8')
    print(f"  {base_path}/index.html")


def genereer_search_index(config: dict, base_path: Path):
    entries = []
    for domein in config['domeinen']:
        for lg in domein['leergangen']:
            lg_pad = base_path / domein['slug'] / lg['slug']
            if not lg_pad.exists():
                continue
            for les_dir in lg_pad.iterdir():
                if not les_dir.is_dir():
                    continue
                meta = lees_metadata(les_dir)
                if not meta:
                    continue
                entries.append({
                    "titel": meta.get('titel', les_dir.name),
                    "domein": domein['naam'],
                    "leergang": lg['naam'],
                    "omschrijving": meta.get('extra', ''),
                    "auteur": meta.get('display_name') or meta.get('friendly_name') or meta.get('issue_author', ''),
                    "pad": str(les_dir.relative_to(Path('.'))).replace('\\', '/') + '/index.html',
                })
    (base_path / 'search-index.json').write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"  {base_path}/search-index.json ({len(entries)} lessen geïndexeerd)")


def _style() -> str:
    return """<style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:'Segoe UI',system-ui,sans-serif;background:#f8fafc;color:#1e293b;line-height:1.6}
        .container{max-width:800px;margin:0 auto;padding:2rem 1rem}
        .card{display:block;background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1rem;text-decoration:none;color:#1e293b;transition:transform .15s,box-shadow .15s}
        .card:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,.1)}
        .card h3{margin-bottom:.25rem}
        .muted{color:#64748b;font-size:.9rem}
        .breadcrumb{max-width:800px;margin:.75rem auto;padding:0 1rem;font-size:.85rem;color:#64748b}
        .breadcrumb a{color:#2563eb;text-decoration:none}
        .search-box{margin-bottom:1.5rem}
        .search-box input{width:100%;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:8px;font-size:1rem;outline:none}
        .search-box input:focus{border-color:#2563eb;box-shadow:0 0 0 3px #dbeafe}
    </style>"""


def _footer() -> str:
    return """<footer style="text-align:center;padding:2rem 1rem;color:#64748b;font-size:.85rem;border-top:1px solid #e2e8f0;margin-top:2rem;">
        Gemaakt door Ralph Wagter met <a href="https://claude.ai" style="color:#2563eb;">Claude Code</a>.
        Vrij hergebruik onder <a href="https://eupl.eu/" style="color:#2563eb;">EUPL-1.2</a>.
        <a href="https://github.com/rwrw01/Claudecodedingetjes" style="color:#2563eb;">GitHub</a>
    </footer>"""


def main():
    config = yaml.safe_load(Path('leergangen.yml').read_text(encoding='utf-8'))
    base_path = Path('leergangen')
    base_path.mkdir(exist_ok=True)

    print("Genereer leergang-indexpagina's...")
    genereer_hoofdindex(config, base_path)
    for domein in config['domeinen']:
        genereer_domein_index(domein, base_path)
        for leergang in domein['leergangen']:
            genereer_leergang_index(domein, leergang, base_path)
    genereer_search_index(config, base_path)
    print("Klaar.")


if __name__ == '__main__':
    main()
