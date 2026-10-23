from flask import (
    Flask, abort, flash, jsonify, redirect, render_template,
    request, session, url_for
)

app = Flask(__name__)


app.secret_key = "c90799551783cb1eeee6bfc99107102512e2f831a9630220fc268f03a371cc99"

taches = [
    {"id": 1, "titre": "Réviser les décorateurs", "priorite": "haute", "terminee": False},
    {"id": 2, "titre": "Installer Flask", "priorite": "normale", "terminee": True},
    {"id": 3, "titre": "Lire la doc Jinja2", "priorite": "basse", "terminee": False},
]

PRIORITES = {"basse", "normale", "haute"}


@app.route("/")
def index():

    filtre = request.args.get("filtre")
    if filtre is None:
        filtre = session.get("filtre", "toutes")

    if filtre not in {"toutes", "actives", "terminees"}:
        filtre = "toutes"

    session["filtre"] = filtre

    if filtre == "actives":
        taches_affichees = [t for t in taches if not t["terminee"]]
    elif filtre == "terminees":
        taches_affichees = [t for t in taches if t["terminee"]]
    else:
        taches_affichees = taches

    restantes = sum(1 for t in taches if not t["terminee"])
    return render_template(
        "taches.html",
        taches=taches_affichees,
        restantes=restantes,
        filtre=filtre,
    )


@app.route("/taches/<int:id>")
def detail_tache(id):
    tache = next((t for t in taches if t["id"] == id), None)
    if tache is None:
        abort(404)
    return render_template("detail.html", tache=tache)


@app.route("/taches/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        priorite = request.form.get("priorite", "normale").strip()

        erreurs = []
        if not titre:
            erreurs.append("Le titre est obligatoire.")
        if len(titre) > 80:
            erreurs.append("Le titre ne doit pas dépasser 80 caractères.")
        if priorite not in PRIORITES:
            erreurs.append("La priorité doit être basse, normale ou haute.")

        if any(t["titre"].casefold() == titre.casefold() for t in taches):
            erreurs.append("Une tâche portant déjà ce titre existe.")

        if erreurs:
            return render_template(
                "ajouter.html", erreurs=erreurs, titre_saisi=titre,
                priorite_saisie=priorite
            ), 400

        nouvel_id = max((t["id"] for t in taches), default=0) + 1
        taches.append({
            "id": nouvel_id,
            "titre": titre,
            "priorite": priorite,
            "terminee": False,
        })
        flash("Tâche ajoutée", "success")
        return redirect(url_for("index"))

    return render_template("ajouter.html", erreurs=[], titre_saisi="", priorite_saisie="normale")


@app.post("/taches/<int:id>/terminer")
def terminer(id):
    tache = next((t for t in taches if t["id"] == id), None)
    if tache is None:
        abort(404)
    tache["terminee"] = True
    flash("Tâche marquée comme terminée.", "success")
    return redirect(url_for("index"))


@app.post("/taches/<int:id>/supprimer")
def supprimer(id):
    tache = next((t for t in taches if t["id"] == id), None)
    if tache is None:
        abort(404)
    taches.remove(tache)
    flash("Tâche supprimée.", "success")
    return redirect(url_for("index"))


@app.route("/api/taches")
def api_taches():
    return jsonify(taches)


@app.errorhandler(404)
def page_introuvable(erreur):
    return render_template("404.html"), 404


if __name__ == "__main__":

    app.run(debug=True)
