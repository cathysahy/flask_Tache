## Mission 1 — Faire tourner Flask
- **Essayé :** lancer avec `flask --app app run`, modifier le titre HTML renvoyé, puis relancer avec `--debug`.
- **Observé :** sans le mode debug, le serveur ne recharge pas automatiquement le code après une modification ; avec `--debug`, le serveur redémarre lors de la sauvegarde.
- **Erreur volontaire :** ajouter une chaîne et un entier avec `"<h1>Mes tâches</h1>" + 1` provoque une erreur Python de type `TypeError`. Le navigateur affiche une erreur serveur et le terminal fournit la trace.
- **Explication :** `--debug` active le rechargement automatique et un débogueur détaillé. Il ne faut pas l'utiliser en production car le débogueur peut exposer l'exécution de code. `--app` peut être omis quand Flask détecte automatiquement `app.py`.
- **Documentation :** Flask Quickstart — A Minimal Application ; Debug Mode.

## Mission 2 — Jouer avec les URL
- **Essayé :** `/taches/2` avec la route `/taches/<id>`, puis avec `/taches/<int:id>` ; essayer `/taches/abc`, `/taches/2/` et `/taches/99`.
- **Observé :** avec `<id>`, `id` est une chaîne (`"2"`), alors que les identifiants de la liste sont des entiers ; la comparaison échoue. Avec `<int:id>`, Flask convertit le segment en entier. `/taches/abc` ne correspond pas à cette route et renvoie 404. La barre oblique finale peut provoquer une redirection selon la route.
- **Explication :** `abort(404)` renvoie le vrai statut HTTP 404. Un simple texte « Tâche introuvable » renvoyé normalement est généralement accompagné du statut 200, qui indique à tort que la requête a réussi.
- **Documentation :** Flask Quickstart — Variable Rules ; Unique URLs / Redirection Behavior ; Redirects and Errors.

## Mission 3 — Afficher les tâches
- **Essayé :** afficher la liste entière, utiliser une boucle, `loop.index`, des filtres et une variable inconnue.
- **Observé :** la liste brute s'affiche sous sa représentation Python. La boucle affiche chaque tâche. Jinja permet l'accès aux clés d'un dictionnaire avec une notation par point (`t.titre`) ou par crochets. Une variable inconnue affiche normalement une valeur vide. Les filtres comme `upper`, `length` et `sort(attribute="titre")` transforment ou ordonnent les valeurs.
- **Sécurité :** un titre contenant `<b>Important</b>` est échappé par défaut dans un template HTML ; il apparaît comme texte et ne devient pas une balise active. Cet échappement protège contre l'injection HTML.
- **Compteur :** `{{ taches|rejectattr("terminee")|list|length }}` compte les tâches non terminées.
- **Explication :** `{{ ... }}` affiche une valeur ; `{% ... %}` exécute une instruction de template comme une boucle ou une condition.
- **Documentation :** Flask Quickstart — Rendering Templates ; Jinja — Variables, For, Builtin Filters, HTML Escaping.

## Mission 4 — Un menu commun
- **Essayé :** créer `base.html`, faire hériter `taches.html`, ajouter un texte hors bloc, un bloc de titre, `super()` et une feuille CSS.
- **Observé :** `{% extends "base.html" %}` hérite de la structure du template de base. Le contenu propre à la page doit être placé dans les blocs définis par le parent ; le texte hors bloc n'est pas inséré dans le bloc de contenu attendu. `super()` conserve le contenu du bloc parent. Flask cherche les pages dans `templates/` et les fichiers statiques dans `static/`.
- **Explication :** l'héritage évite de recopier le menu et la structure HTML sur chaque page. `url_for('static', filename='style.css')` construit l'URL de la feuille CSS.
- **Documentation :** Jinja — Template Inheritance ; Flask Quickstart — Static Files, Rendering Templates.

## Mission 5 — Ajouter une tâche
- **Essayé :** soumettre le formulaire, actualiser avec F5, observer l'onglet Réseau, tester un titre vide, un titre trop long, une priorité invalide et une clé de formulaire incorrecte.
- **Observé :** sans redirection, actualiser après un POST peut demander de renvoyer le formulaire et créer un doublon. Avec `redirect(url_for("index"))`, le navigateur reçoit typiquement une réponse 302 après POST, puis effectue un GET qui reçoit 200 ; F5 répète le GET, pas l'ajout.
- **Validation :** le serveur refuse un titre vide, un titre dépassant 80 caractères ou une priorité autre que `basse`, `normale` ou `haute`. Cette version refuse aussi un titre déjà utilisé.
- **Explication :** `request.form.get("titre", "")` permet une valeur par défaut si le champ manque ; `request.form["titre"]` peut provoquer une erreur `BadRequestKeyError` si la clé est absente. Un formulaire envoyé en GET place généralement les champs dans la chaîne de requête de l'URL.
- **Documentation :** Flask Quickstart — HTTP Methods ; Accessing Request Data ; Redirects and Errors.

## Mission 6 — Messages et mémoire
- **Essayé :** appeler `flash()` sans clé secrète, définir `app.secret_key`, afficher les messages, choisir un filtre et ouvrir une fenêtre privée.
- **Observé :** sans clé secrète, Flask lève une erreur lors de l'utilisation des messages flash ou de la session. Avec une clé, le message s'affiche après l'ajout puis disparaît après sa lecture lors de la requête suivante. Le filtre est conservé dans la session du navigateur ; une fenêtre privée possède une session/cookie distinct.
- **Cookie :** le cookie de session Flask est signé. Modifier sa valeur invalide généralement la signature et Flask ignore le contenu modifié.
- **Explication :** `flash()` transmet un message temporaire à la requête suivante. La session Flask par défaut est stockée côté navigateur dans un cookie signé, pas chiffré ; il ne faut donc pas y placer des secrets.
- **Documentation :** Flask Quickstart — Sessions ; Message Flashing ; URL Building.

## Bonus
1. **Terminer / supprimer :** les boutons envoient des requêtes POST. Des liens GET ne devraient pas modifier ou supprimer des données, car les navigateurs, robots ou préchargements peuvent suivre des liens sans intention de modification.
2. **Page 404 :** `@app.errorhandler(404)` affiche un template personnalisé tout en renvoyant le statut HTTP 404.
3. **API :** `/api/taches` renvoie les tâches au format JSON avec le type de contenu approprié, généralement `application/json`.
