# Compétences de production des podcasts Dev’Obs

Ce dépôt rassemble les compétences Codex utilisées pour produire les podcasts de l’organisation `dev-obs`.

## Catalogue

| Podcast | Compétence | Ce qu’elle permet de faire |
| --- | --- | --- |
| Dev’Obs | [`$devobs-dans-le-retro`](skills/devobs-dans-le-retro/SKILL.md) | Récupérer les pistes Craig, monter l’ouverture et la fin, produire le master dans Auphonic, préparer les sous-titres et les chapitres, puis vérifier un brouillon Transistor. |
| Dans Ton Kube | À documenter | Le dépôt de l’émission reste la référence de production. [Dans Ton Kube](https://github.com/dev-obs/DTK) |

## Reprendre le montage sur une autre machine

1. Depuis le dossier du nouvel épisode, installez la compétence pour Codex avec `npx` et un compte GitHub qui a accès au dépôt privé.

   ```sh
   npx skills add dev-obs/podcast-skills --skill devobs-dans-le-retro --agent codex
   ```

   Si GitHub n’est pas encore authentifié sur la machine, connectez-vous avec `gh auth login` ou configurez vos identifiants Git habituels. Ajoutez `--global` si vous souhaitez utiliser la compétence dans tous vos dossiers d’épisode. [Documentation de `npx skills add`](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add)

2. Rendez les fichiers du nouvel épisode accessibles sur cette machine. Pour démarrer, il suffit du lien Craig accessible ou de pistes FLAC synchronisées, avec les noms des intervenants si les fichiers sont ambigus. Si le traitement a déjà commencé, munissez-vous des références Auphonic et Transistor existantes.
3. Pour le montage local, installez FFmpeg avec `ffprobe`. Python 3 sert à contrôler le WebVTT. Pour aller jusqu’au brouillon, connectez-vous aux comptes Auphonic et Transistor de Dev’Obs. Le montage peut passer par NyxMix ou s’effectuer directement avec FFmpeg. Les tableaux de bord fonctionnent aussi si les connecteurs Codex manquent.
4. Ouvrez le dossier de l’épisode dans Codex et lancez la compétence avec le périmètre voulu. Par exemple, « Utilise `$devobs-dans-le-retro` pour monter ces pistes et me livrer les FLAC synchronisés » ou « Utilise `$devobs-dans-le-retro` pour préparer cet enregistrement jusqu’au brouillon Transistor. »

## Organisation

Chaque compétence est autonome dans `skills/<podcast>-<format>/`. On utilise le préfixe `devobs-` pour Dev’Obs et `dtk-` pour Dans Ton Kube. Le `SKILL.md` décrit le déroulé et renvoie aux références et scripts propres au format.

Travaillez dans un dossier séparé pour chaque épisode. Le dépôt contient les consignes et les outils réutilisables. Les pistes, exports, notes éditoriales, fichiers de reprise, liens signés et identifiants de connexion restent dans le dossier de l’épisode ou dans les comptes de production.
