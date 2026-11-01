# Jimmy Décrypte — Reel #05 : fact-check, tes jeux mobiles te suivent ?

Reel 9:16 (1080×1920, 30 fps, 46 s), sans voix, fait en code avec le moteur commun `../lib/kit.js`. C'est le fact-check d'un post Instagram viral, limité aux affirmations qui touchent à la cybersécurité.

- **Vidéo :** [`reel.mp4`](reel.mp4)
- **Couverture :** [`cover.png`](cover.png)
- **Légende, hashtags et sources :** [`legende.md`](legende.md)

## Storyboard

| Temps | Scène | Ce qu'on voit |
|---|---|---|
| 0–4,5 s | Accroche | Carte du post viral (5 jeux, j'aime qui défilent). « Ce post viral accuse tes jeux mobiles. ON A VÉRIFIÉ. » |
| 4,5–9 s | Les affirmations | A « Ces jeux collectent tes données. » B « Des applis s'installent sans ton accord. » Mention : la géopolitique n'est pas notre sujet |
| 9–21 s | A : VRAI | Fiche « Confidentialité de l'app » de Coin Master, puis 3 cartes (Coin Master, Woodoku, Wordscapes) avec leurs vraies données de suivi, puis réseau publicitaire. Tampon VRAI |
| 21–31 s | B : NUANCÉ | Un téléphone neuf se configure, des applis apparaissent seules, puis AppCloud. Pas ces jeux, mais AppCloud sur des Samsung A et M (Moyen-Orient, Afrique du Nord, SMEX 2025). Tampon NUANCÉ |
| 31–41,5 s | Protège-toi | 4 cartes « chemin de réglages » qui se tapent comme un fil d'Ariane |
| 41,5–46 s | Fin | « Gratuit ne veut pas dire sans prix. » |

## Reconstruire

```bash
python3 audio.py && node render.mjs frames 30 4 && node render.mjs cover
ffmpeg -framerate 30 -i frames/f_%05d.png -i audio.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -shortest reel.mp4
```

Les icônes de jeux sont génériques (initiales), sans aucun logo officiel. Sons d'interface : uisfx (CC0). Musique, tampons et petits sons de jeu : synthèse originale.
