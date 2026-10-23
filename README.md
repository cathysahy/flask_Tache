## 1. Pré-requis
- Python 3.11 ou plus
- Git (pour les commits demandés)
- Un navigateur web

## 2. Installation sur Kali Linux / Debian
Dans un terminal, placez-vous dans ce dossier puis exécutez :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si la création du venv échoue sur Kali, vérifiez que `python3-venv` est installé.

## 3. Lancement
```bash
flask --app app run --debug
```
Ouvrez http://127.0.0.1:5000. Arrêtez le serveur avec Ctrl+C.

Alternative : `python app.py`.

**Attention :** le mode debug est uniquement destiné au développement local, jamais à la production. La clé secrète dans `app.py` est une valeur de TP ; générez-en une vraie pour un usage plus sérieux.

## 4. Pages à tester
- `/` : liste des tâches
- `/taches/2` : détail de la tâche 2
- `/taches/99` : page 404 personnalisée avec statut HTTP 404
- `/taches/ajouter` : formulaire d'ajout avec validation
- `/?filtre=actives`, `/?filtre=terminees`, `/?filtre=toutes` : filtres
- `/api/taches` : API JSON

Les données sont stockées en mémoire : elles reviennent à leur état initial au redémarrage du serveur. La persistance en base de données est prévue pour une séance ultérieure.

## 5. Missions et Git
Le support demande un commit clair par mission. Exemple :
```bash
git init
git add .
git commit -m "mission 1 : faire tourner Flask"
```
Après chaque mission, adaptez `git add` et le message du commit. Si Git demande votre identité, configurez `user.name` et `user.email`.

## 6. Limites pédagogiques
- Cette solution réunit les fonctionnalités finales pour que vous puissiez tester le TP complet.
- Pour respecter la méthode de découverte du cours, réalisez les essais décrits dans `JOURNAL.md` et observez vous-même les codes HTTP et les messages.
- Il n'y a pas de base de données dans cette séance.
