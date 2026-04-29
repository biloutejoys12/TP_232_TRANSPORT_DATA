from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_PATH = "transport_yaounde.db"

# --- Initialisation de la base de données ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            age INTEGER NOT NULL,
            type_transport TEXT NOT NULL,
            temps_attente INTEGER NOT NULL,
            prix REAL NOT NULL,
            confort INTEGER NOT NULL CHECK(confort BETWEEN 1 AND 5),
            date_collecte TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- Routes ---

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "API Transport Yaoundé opérationnelle"})


@app.route("/api/enquetes", methods=["POST"])
def creer_enquete():
    data = request.get_json()

    required = ["nom", "age", "type_transport", "temps_attente", "prix", "confort"]
    for field in required:
        if field not in data:
            return jsonify({"erreur": f"Champ manquant : {field}"}), 400

    # Validations
    if not (1 <= int(data["age"]) <= 120):
        return jsonify({"erreur": "Âge invalide (1-120)"}), 400
    if int(data["temps_attente"]) < 0:
        return jsonify({"erreur": "Temps d'attente invalide"}), 400
    if float(data["prix"]) < 0:
        return jsonify({"erreur": "Prix invalide"}), 400
    if not (1 <= int(data["confort"]) <= 5):
        return jsonify({"erreur": "Confort invalide (1-5)"}), 400

    transports_valides = ["bus", "taxi", "moto_taxi", "voiture_personnelle", "marche_a_pied", "autre"]
    if data["type_transport"] not in transports_valides:
        return jsonify({"erreur": f"Type de transport invalide. Valeurs: {transports_valides}"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO enquetes (nom, age, type_transport, temps_attente, prix, confort, date_collecte)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["nom"].strip(),
        int(data["age"]),
        data["type_transport"],
        int(data["temps_attente"]),
        float(data["prix"]),
        int(data["confort"]),
        datetime.now().isoformat()
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"message": "Enquête enregistrée avec succès", "id": new_id}), 201


@app.route("/api/enquetes", methods=["GET"])
def lister_enquetes():
    transport = request.args.get("transport")
    conn = get_db()
    cursor = conn.cursor()

    if transport:
        cursor.execute("SELECT * FROM enquetes WHERE type_transport = ? ORDER BY date_collecte DESC", (transport,))
    else:
        cursor.execute("SELECT * FROM enquetes ORDER BY date_collecte DESC")

    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/api/statistiques", methods=["GET"])
def statistiques():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM enquetes")
    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT type_transport,
               COUNT(*) as nombre,
               AVG(temps_attente) as moy_attente,
               AVG(prix) as moy_prix,
               AVG(confort) as moy_confort,
               AVG(age) as moy_age
        FROM enquetes
        GROUP BY type_transport
        ORDER BY nombre DESC
    """)
    par_transport = [dict(row) for row in cursor.fetchall()]

    cursor.execute("SELECT AVG(age) as moy_age, AVG(temps_attente) as moy_attente, AVG(prix) as moy_prix, AVG(confort) as moy_confort FROM enquetes")
    globales = dict(cursor.fetchone())

    conn.close()
    return jsonify({
        "total_enquetes": total,
        "moyennes_globales": globales,
        "par_transport": par_transport
    })


@app.route("/api/enquetes/<int:enquete_id>", methods=["DELETE"])
def supprimer_enquete(enquete_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM enquetes WHERE id = ?", (enquete_id,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"erreur": "Enquête non trouvée"}), 404
    conn.commit()
    conn.close()
    return jsonify({"message": "Enquête supprimée"})


if __name__ == "__main__":
    init_db()
    print("🚀 API Transport Yaoundé démarrée sur http://localhost:5000")
   
