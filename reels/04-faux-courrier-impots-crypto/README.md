# Jimmy Décrypte — Reel #04 : le faux courrier des impôts qui vise les cryptos

Reel d'actualité 9:16 (1080×1920, 30 fps, 46 s), sans voix, entièrement fait en code avec le moteur commun `../lib/kit.js`.

- **Vidéo :** [`reel.mp4`](reel.mp4)
- **Couverture :** [`cover.png`](cover.png)
- **Légende, hashtags et sources :** [`legende.md`](legende.md)

## L'actualité

Le 29 octobre 2026, la Police nationale alerte sur un faux courrier de la DGFiP envoyé par la poste. C'est une « mise en demeure » de déclarer ses cryptoactifs, avec un QR code qui mène à un clone d'impots.gouv.fr. Ce faux site demande la phrase de récupération du portefeuille. Le même jour, Binance se fait voler environ 6,3 milliards de dollars, le plus gros vol de cryptos jamais enregistré. Aucun lien n'est établi entre les deux : la vidéo les présente comme deux faits du même jour.

## Storyboard

| Temps | Scène | Ce qu'on voit |
|---|---|---|
| 0–4 s | Accroche | Une enveloppe tombe, un tampon « MISE EN DEMEURE » s'écrase. « Ce courrier "des impôts" peut vider ton portefeuille crypto. » |
| 4–10 s | L'actualité | 29 OCTOBRE 2026 : Binance (≈ 6,3 milliards $) et, le même jour, l'alerte de la Police nationale |
| 10–21 s | Le courrier | L'enveloppe s'ouvre, le courrier se remplit (marqué RECONSTITUTION), annotations : urgence, menace d'amende, vraies références. Scan du QR, l'adresse du site s'affiche : « Ce n'est pas impots.gouv.fr. » |
| 21–31 s | Le piège | Le faux portail demande les 12 mots, qui s'envolent vers le serveur des escrocs ; le portefeuille se vide jusqu'à 0,00 € |
| 31–41,5 s | Réflexes | 5 feuilles de papier, chacune tamponnée |
| 41,5–46 s | Fin | « Les impôts ne demandent JAMAIS ta phrase de récupération. » |

## Reconstruire

```bash
python3 audio.py && node render.mjs frames 30 4 && node render.mjs cover
ffmpeg -framerate 30 -i frames/f_%05d.png -i audio.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -shortest reel.mp4
```

Sons d'interface : uisfx (CC0, `sfx/LICENSE-AUDIO`). Papier, tampons et musique : synthèse originale. Le courrier, le QR code (factice, non décodable), l'adresse `impots-portail-actifs.exemple`, les 12 mots et le solde sont fictifs.
