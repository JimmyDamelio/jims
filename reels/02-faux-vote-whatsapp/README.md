# Jimmy Décrypte — Reel #02 : le faux vote WhatsApp

Reel d'actualité 9:16 (1080×1920, 30 fps, 46 s), sans voix, entièrement fait en code. Il réutilise le moteur graphique commun `../lib/kit.js` (extrait du Reel #01) et les polices de `../lib/fonts/`.

- **Vidéo :** [`reel.mp4`](reel.mp4)
- **Couverture :** [`cover.png`](cover.png)
- **Légende, hashtags et sources :** [`legende.md`](legende.md)

## L'actualité

Une campagne de piratage de comptes WhatsApp se propage en France.

1. Un proche, dont le compte est déjà piraté, demande de voter pour un concours de danse, une bourse d'études ou un enfant.
2. Le faux site demande ton numéro, puis te donne un « code de vote ».
3. Ce code est en réalité le code qui sert à **associer un nouvel appareil** à ton compte.
4. L'escroc lit alors tes conversations, écrit à tes proches en ton nom, et l'arnaque repart.

Dates : alerte de la Gendarmerie nationale le 26 octobre 2026, puis alerte Cybermalveillance.gouv.fr publiée le 27 octobre 2026 (mise à jour ensuite).

## Storyboard

| Temps | Scène | Ce qu'on voit |
|---|---|---|
| 0–4 s | Accroche | Message de « Julie » avec un lien de vote. « Ce message vient d'un proche. C'est une arnaque. » Badge ALERTE 27 OCT. 2026 |
| 4–10 s | Ce qui se passe | Fiche « En ce moment » ; sources Gendarmerie 26/10 et Cybermalveillance 27/10 ; prétextes : concours de danse, bourse d'études, aider un enfant |
| 10–22 s | Démonstration | Lien, faux site de vote, numéro, « code de vote », écran « Associer un appareil », code tapé. Glitch : un ordinateur inconnu s'allume |
| 22–30,5 s | Conséquences | L'ordinateur lit les conversations, écrit en ton nom, demande de l'argent, puis le réseau de contacts s'infecte en boule de neige. « Concerné : tout utilisateur de WhatsApp » |
| 30,5–41,5 s | Se protéger | Parcours Paramètres › Appareils connectés › déconnecter l'inconnu, puis 5 réflexes |
| 41,5–46 s | Fin | « UN CODE WHATSAPP ne sert jamais à voter. » Appel au partage, logo, sources |

Tous les repères de temps sont dans `timeline.js`, lu à la fois par l'image et par le son.

## Reconstruire

```bash
python3 audio.py                 # -> audio.wav
node render.mjs frames 30 4      # -> frames/ (1380 PNG)
node render.mjs cover            # -> cover.png
ffmpeg -framerate 30 -i frames/f_%05d.png -i audio.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -shortest reel.mp4
```

Aperçu dans un navigateur : `film.html?play`, `film.html?t=19.5` ou `film.html?cover`.

## Licences

- Polices : Inter et Space Grotesk (OFL 1.1).
- Sons d'interface : uisfx « studio » (CC0, `sfx/LICENSE-AUDIO`).
- Musique et impacts : synthèse originale.
- « Julie », « Léa », le concours, le code et le message d'argent sont **fictifs**. C'est une simulation, pas une capture réelle.
