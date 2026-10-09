# Silend CMS-Demo – Café Mahlwerk

Test, wie Kunden ihre Website selbst bearbeiten können (für das Business-Paket). Café Mahlwerk ist fiktiv.

## So funktioniert es

```
Kunde ändert Text in Pages CMS  →  Commit auf GitHub  →  GitHub Actions baut die Seite  →  nach ca. 1 Minute online
```

| Datei | Zweck |
| --- | --- |
| `content/startseite.json` | Alle Inhalte (Texte, Öffnungszeiten, Karte, Aktuelles) |
| `.pages.yml` | Welche Felder der Kunde in Pages CMS sieht und wie sie heißen |
| `template.html` + `style.css` | Design – kann der Kunde **nicht** ändern |
| `build.py` | Setzt Inhalte ins Template ein → `_site/` |
| `.github/workflows/deploy.yml` | Baut und veröffentlicht bei jedem Push auf GitHub Pages |

Lokal ansehen: `python3 build.py`, dann `_site/index.html` im Browser öffnen.

## Einrichtung (einmalig)

1. Repo auf GitHub: **Settings → Pages → Source: GitHub Actions**
2. https://app.pagescms.org öffnen, mit GitHub anmelden, Zugriff auf dieses Repo erlauben
3. Repo auswählen → links erscheint „Startseite“ → bearbeiten → **Save**
4. Unter **Actions** sieht man den Build; danach ist die Änderung live

Für echte Kunden: Kunde bekommt in Pages CMS eine Einladung per E-Mail (Collaborators) und braucht **kein** GitHub-Konto.
