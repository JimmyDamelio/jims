# Jimmy Décrypte — Reel #01 : « Validez pour annuler »

Reel Instagram 9:16 (1080×1920, 30 fps, 35 s), sans voix. Tout est fait en code : l'image est dessinée en Canvas 2D dans Chromium, la musique et les impacts sont synthétisés en Python, les bruits d'interface sont des enregistrements uisfx (CC0).

- **Vidéo :** [`reel.mp4`](reel.mp4)
- **Couverture :** [`cover.png`](cover.png)
- **Légende + hashtags :** [`legende.md`](legende.md)

## Sujet

L'arnaque au faux conseiller bancaire : « Un paiement suspect est en cours. Pour l'annuler, validez-le dans votre appli. » En réalité, valider, c'est autoriser le paiement.

Source : Banque de France, page « Fraude aux moyens de paiement ». La banque ne demande jamais « ni code, ni mot de passe ni identifiant, ni d'effectuer ou de valider des opérations ». Elle « n'a besoin d'aucune action de votre part pour bloquer une transaction ».

## Storyboard

| Temps | Scène | À l'écran | Son |
|---|---|---|---|
| 0–4 s | Accroche | Appel entrant « Service Fraude · Ta Banque ». « Il ne va rien te voler. C'est toi qui vas valider. » | sonnerie, vibrations, tap |
| 4–10,5 s | Situation | L'appel : bulles de texte de l'appelant (aucune voix), puce « Il te presse » | pouls grave, pops de messages |
| 10,5–15,2 s | Démonstration | Notification, app bancaire, 1 890,00 €, le doigt approche « Valider » | notification, compteur, montée |
| 15,2–20 s | Révélation | Gel + glitch. « VALIDER = AUTORISER », le bouton se décrypte, les € s'envolent | impact, glitch, erreur |
| 20–26,5 s | Règle | « Ta banque ne te demandera JAMAIS : » ×3, citation Banque de France | croix, info |
| 26,5–31,5 s | Réflexes | 1. Raccroche. 2. Rappelle ta banque toi-même. 3. Déjà validé ? Opposition | raccrochage, clics |
| 31,5–35 s | Fin | « VALIDER ≠ ANNULER », partage, logo qui se décrypte | impact, frappe, succès |

Toutes les heures de repère sont dans `timeline.js`, lu à la fois par l'image et par le son.

## Reconstruire

Il faut Node, Playwright (Chromium), Python 3 avec numpy, et ffmpeg.

```bash
python3 audio.py                 # -> audio.wav
node render.mjs frames 30 4      # -> frames/ (1050 PNG)
node render.mjs cover            # -> cover.png
ffmpeg -framerate 30 -i frames/f_%05d.png -i audio.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -shortest reel.mp4
```

Aperçu dans un navigateur : `film.html?play`, `film.html?t=16.5` (un instant précis) ou `film.html?cover`.

## Licences

- Polices : Inter et Space Grotesk (SIL OFL 1.1, via Fontsource).
- Sons d'interface : uisfx « studio » (CC0 1.0, `sfx/LICENSE-AUDIO`).
- Musique, sonnerie, impacts : synthèse originale (`audio.py`).
