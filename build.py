"""Baut die Seite: content/startseite.json + template.html -> _site/index.html.

Nur Python-Standardbibliothek, damit es lokal und in GitHub Actions ohne
Installation läuft. Aufruf: python3 build.py
"""
import json
import shutil
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / '_site'


def absaetze(text):
    """Mehrzeiliger Text -> <p>-Absätze (Leerzeile = neuer Absatz)."""
    teile = [t.strip() for t in (text or '').split('\n\n') if t.strip()]
    return ''.join(f'<p>{escape(t).replace(chr(10), "<br>")}</p>' for t in teile)


def datum_de(wert):
    try:
        return date.fromisoformat(str(wert)[:10]).strftime('%d.%m.%Y')
    except ValueError:
        return escape(str(wert or ''))


def main():
    c = json.loads((ROOT / 'content' / 'startseite.json').read_text(encoding='utf-8'))

    karte = ''.join(
        f'<li><strong>{escape(k.get("name", ""))}</strong>'
        f'<span>{escape(k.get("beschreibung", ""))}</span>'
        f'<span class="preis">{escape(k.get("preis", ""))}</span></li>'
        for k in c.get('karte') or []
    )
    zeiten = ''.join(
        f'<dt>{escape(z.get("tage", ""))}</dt><dd>{escape(z.get("zeit", ""))}</dd>'
        for z in c.get('oeffnungszeiten') or []
    )
    news = sorted(c.get('aktuelles') or [], key=lambda n: str(n.get('datum', '')), reverse=True)
    aktuelles = ''.join(
        f'<article><time>{datum_de(n.get("datum"))}</time>'
        f'<h3>{escape(n.get("titel", ""))}</h3>{absaetze(n.get("text"))}</article>'
        for n in news
    ) or '<p>Gerade gibt es nichts Neues.</p>'
    hinweis = (c.get('hinweis') or '').strip()

    werte = {
        'name': escape(c.get('name', '')),
        'titel': escape(c.get('titel', '')),
        'untertitel': escape(c.get('untertitel', '')),
        # Pages CMS speichert Bildpfade evtl. mit führendem "/" – relativ machen,
        # damit es auch unter einem Unterordner (GitHub Pages) funktioniert.
        'bild': escape((c.get('bild') or '').lstrip('/')),
        'hinweis': f'<p class="hinweis">{escape(hinweis)}</p>' if hinweis else '',
        'karte': karte,
        'oeffnungszeiten': zeiten,
        'aktuelles': aktuelles,
        'adresse': escape(c.get('adresse', '')),
        'email': escape(c.get('email', '')),
    }

    html = (ROOT / 'template.html').read_text(encoding='utf-8')
    for key, wert in werte.items():
        html = html.replace('{{' + key + '}}', wert)

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / 'index.html').write_text(html, encoding='utf-8')
    shutil.copy(ROOT / 'style.css', OUT / 'style.css')
    shutil.copytree(ROOT / 'images', OUT / 'images')
    print('Fertig: _site/index.html')


if __name__ == '__main__':
    main()
