# 📺 YouTube Downloader - Pro

**YTD Pro** est une application permettant de télécharger facilement des vidéos et des playlists entières depuis YouTube.


## 🚀 Fonctionnalités

- **Téléchargement Polyvalent** : Supporte les vidéos (MP4) et l'extraction audio (MP3).
- **Support Playlist** : Télécharge automatiquement toutes les vidéos d'une playlist.
- **Organisation Automatique** : Crée des dossiers structurés basés sur le nom de la playlist ou de la vidéo.
- **Anti-Doublons** : Système intelligent (`archive.txt`) pour ignorer les vidéos déjà téléchargées lors des mises à jour de playlist.
- **Haute Qualité** : Utilise `yt-dlp` pour obtenir la meilleure qualité vidéo et audio disponible (320kbps pour l'audio).
- **Interface Moderne** : GUI basée sur `ttkbootstrap` (thème Superhero).
- **Portable** : Inclut `ffmpeg` et `ffprobe` pour une conversion sans configuration complexe.

## 🛠️ Installation et Prérequis

### Utilisateurs Standard
Si vous utilisez la version compilée (`YTD-Pro.exe`) :
1. Téléchargez ou décompressez le dossier du projet.
2. Assurez-vous que le dossier `utils` contient bien `ffmpeg.exe` et `ffprobe.exe`.
3. Lancez simplement **`start.bat`** ou **`YTD-Pro.exe`**.

### Pour les Développeurs (Source)
Si vous souhaitez exécuter le script Python directement :

1. **Prérequis** :
   - Python 3.x installé.
   - Les fichiers binaires `ffmpeg.exe` et `ffprobe.exe` placés dans le dossier `utils/`.

2. **Installation des dépendances** :
   Lancez le script `setup.bat`.
   Il est situé dans le dossier `utils/`.
## 📖 Utilisation

### Pour les utilisateurs qui ont python installé
1. **Lancer l'application** : Double-cliquez sur `start.bat`.
2. **Coller le lien** : Insérez l'URL de la vidéo ou de la playlist YouTube dans le champ dédié.
3. **Choisir le format** : Sélectionnez **Vidéo MP4** ou **Audio MP3**.
4. **Télécharger** : Cliquez sur le bouton "⚡ LANCER ⚡".
5. **Résultat** : Les fichiers seront enregistrés dans le dossier `playlist_&_videos` à la racine du projet.

### Pour les utilisateurs qui n'ont pas python installé
1. **Lancer l'application** : Double-cliquez sur `YTD-Pro.exe`.
2. **Coller le lien** : Insérez l'URL de la vidéo ou de la playlist YouTube dans le champ dédié.
3. **Choisir le format** : Sélectionnez **Vidéo MP4** ou **Audio MP3**.
4. **Télécharger** : Cliquez sur le bouton "⚡ LANCER ⚡".
5. **Résultat** : Les fichiers seront enregistrés dans le dossier `playlist_&_videos` à la racine du projet.

## 📂 Structure du Projet

```
.
├── YTD-Pro.exe           # Exécutable principal (si compilé)
├── start.bat             # Script de lancement rapide
├── playlist_&_videos/    # Dossier de destination des téléchargements
└── utils/                # Dossier système
    ├── main.py           # Code source principal
    ├── ffmpeg.exe        # Moteur de conversion vidéo
    ├── ffprobe.exe       # Outil d'analyse média
    ├── archive.txt       # Historique des téléchargements (anti-doublons)
    └── requierments.txt  # Liste des librairies Python
```

## ⚙️ Compilation (Build)

Pour compiler l'application en un fichier `.exe` autonome, utilisez la commande suivante à la racine :

```bash
python -m PyInstaller --noconsole --onefile --name "YTD-Pro" utils/main.py
```
*Note : Assurez-vous d'inclure les dépendances binaires (ffmpeg) si nécessaire ou de les placer à côté de l'exécutable.*

## 🤝 Crédits

Propulsé par :
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
