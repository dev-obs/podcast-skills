# Compétences de production des podcasts Dev’Obs

Ce dépôt rassemble les compétences Codex utilisées pour produire les podcasts de l’organisation `dev-obs`.

## Catalogue

| Podcast | Compétence | Ce qu’elle permet de faire |
| --- | --- | --- |
| Dev’Obs | [`$devobs-dans-le-retro`](.agents/skills/devobs-dans-le-retro/SKILL.md) | Récupérer les pistes Craig, monter l’ouverture et la fin, produire le master dans Auphonic, préparer les sous-titres et les chapitres, puis vérifier un brouillon Transistor. |
| Dans Ton Kube | À documenter | Le dépôt de l’émission reste la référence de production. [Dans Ton Kube](https://github.com/dev-obs/DTK) |

## Reprendre le montage sur une autre machine

1. Avec un compte qui a accès au dépôt privé, clonez-le et ouvrez le dossier obtenu dans une nouvelle session Codex.

   ```sh
   git clone https://github.com/dev-obs/podcast-skills.git
   cd podcast-skills
   ```

2. Rendez les fichiers du nouvel épisode accessibles sur cette machine. Pour démarrer, il suffit du lien Craig accessible ou de pistes FLAC synchronisées, avec les noms des intervenants si les fichiers sont ambigus. Si le traitement a déjà commencé, munissez-vous des références Auphonic et Transistor existantes.
3. Pour le montage local, installez FFmpeg avec `ffprobe`. Python 3 sert à contrôler le WebVTT. Pour aller jusqu’au brouillon, connectez-vous aux comptes Auphonic et Transistor de Dev’Obs. Le montage peut passer par NyxMix ou s’effectuer directement avec FFmpeg. Les tableaux de bord fonctionnent aussi si les connecteurs Codex manquent.
4. Lancez la compétence avec le périmètre voulu. Par exemple, « Utilise `$devobs-dans-le-retro` pour monter les pistes dans `/chemin/vers/episode` et me livrer les FLAC synchronisés » ou « Utilise `$devobs-dans-le-retro` pour préparer cet enregistrement jusqu’au brouillon Transistor. »

Pour rendre la compétence disponible dans un autre projet, copiez son dossier complet sous `.agents/skills/` dans ce projet ou sous `~/.agents/skills/` pour votre compte. [Documentation Codex sur les compétences](https://developers.openai.com/codex/skills/)

## Organisation

Chaque compétence est autonome dans `.agents/skills/<podcast>-<format>/`. On utilise le préfixe `devobs-` pour Dev’Obs et `dtk-` pour Dans Ton Kube. Le `SKILL.md` décrit le déroulé et renvoie aux références et scripts propres au format.

Travaillez dans un dossier séparé pour chaque épisode. Le dépôt contient les consignes et les outils réutilisables. Les pistes, exports, notes éditoriales, fichiers de reprise, liens signés et identifiants de connexion restent dans le dossier de l’épisode ou dans les comptes de production.
