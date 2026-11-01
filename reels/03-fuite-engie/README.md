# Jimmy Décrypte — Reel #03 : la fuite Engie

Reel d'actualité 9:16 (1080×1920, 30 fps, 46 s), sans voix, entièrement fait en code avec le moteur commun `../lib/kit.js`.

- **Vidéo :** [`reel.mp4`](reel.mp4)
- **Couverture :** [`cover.png`](cover.png)
- **Légende, hashtags et sources :** [`legende.md`](legende.md)

## L'actualité

Le 27 octobre 2026, Engie confirme un « accès inhabituel » à un outil de prospection utilisé par ses partenaires commerciaux. Seuls des clients en France sont concernés et il n'y a pas de données bancaires. Les données exposées, d'après le courriel envoyé aux clients : nom, adresse, e-mail, téléphone, identifiant client, numéro de contrat, PDL/PCE. Le nombre de clients n'est pas communiqué et personne n'a revendiqué l'attaque. Aucune arnaque liée n'est signalée à ce jour : la vidéo présente le risque, pas un fait.

## Storyboard

| Temps | Scène | Ce qu'on voit |
|---|---|---|
| 0–4 s | Accroche | Une fiche client se décrypte. « Il connaît ton nom, ton adresse, ton n° de contrat… Mais ce n'est pas Engie. » |
| 4–12 s | Ce qui s'est passé | Schéma : Engie, puis l'outil d'un partenaire, puis un « accès inhabituel » qui aspire les données. Ce qui est confirmé et ce qui ne l'est pas (puces ✓ et ?) |
| 12–20 s | Ce qui a fuité | Les 7 champs se remplissent. « Tu as reçu un e-mail d'Engie ? Tu es concerné. » Données bancaires : non concernées |
| 20–31 s | Le vrai danger | Les champs volent de la fiche vers un SMS qui s'écrit tout seul (EXEMPLE FICTIF). « Toutes les infos sont vraies. Le message est faux. » |
| 31–41,5 s | Réflexes | 5 cartes plein écran, une par temps fort |
| 41,5–46 s | Fin | « Ils ont tes infos. Pas ta confiance. » Logo, sources |

## Reconstruire

```bash
python3 audio.py && node render.mjs frames 30 4 && node render.mjs cover
ffmpeg -framerate 30 -i frames/f_%05d.png -i audio.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 \
  -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart -shortest reel.mp4
```

Les sons d'interface viennent d'uisfx (CC0, `sfx/LICENSE-AUDIO`). La musique est synthétisée. La cliente, ses données, le SMS et le lien `remb-energie.exemple` sont fictifs.
