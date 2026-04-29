import streamlit as st  # type: ignore[import]
import sqlite3
import pandas as pd  # type: ignore[import]
from datetime import datetime
import os

# ── Configuration page ──
st.set_page_config(
    page_title="TransportData Yaoundé",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS personnalisé ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main { background-color: #0a0e1a; }

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    color: #e8edf5;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

.hero-accent {
    background: linear-gradient(90deg, #f4a935, #e8573a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.badge {
    display: inline-block;
    background: rgba(244,169,53,0.1);
    border: 1px solid rgba(244,169,53,0.3);
    color: #f4a935;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.stat-box {
    background: #111827;
    border: 1px solid #1f2d42;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    margin-bottom: 1rem;
}

.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #f4a935;
}

.stat-label {
    font-size: 0.8rem;
    color: #6b7f96;
    margin-top: 2px;
}

.success-box {
    background: rgba(62,207,142,0.1);
    border: 1px solid rgba(62,207,142,0.3);
    border-radius: 10px;
    padding: 1rem;
    color: #3ecf8e;
    font-weight: 500;
    margin: 1rem 0;
}

.error-box {
    background: rgba(232,87,58,0.1);
    border: 1px solid rgba(232,87,58,0.3);
    border-radius: 10px;
    padding: 1rem;
    color: #e8573a;
    font-weight: 500;
    margin: 1rem 0;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    color: #6b7f96 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

div[data-testid="stTabs"] button {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

.stButton > button {
    background: linear-gradient(135deg, #f4a935, #e8573a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
}

footer { display: none; }
#MainMenu { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Base de données ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "transport_yaounde.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS enquetes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            age INTEGER NOT NULL,
            type_transport TEXT NOT NULL,
            temps_attente INTEGER NOT NULL,
            prix REAL NOT NULL,
            confort INTEGER NOT NULL,
            date_collecte TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_all(transport_filter=None):
    conn = sqlite3.connect(DB_PATH)
    if transport_filter and transport_filter != "Tous":
        df = pd.read_sql_query(
            "SELECT * FROM enquetes WHERE type_transport=? ORDER BY date_collecte DESC",
            conn, params=(transport_filter,)
        )
    else:
        df = pd.read_sql_query("SELECT * FROM enquetes ORDER BY date_collecte DESC", conn)
    conn.close()
    return df

def insert(nom, age, transport, attente, prix, confort):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO enquetes (nom, age, type_transport, temps_attente, prix, confort, date_collecte) VALUES (?,?,?,?,?,?,?)",
        (nom, age, transport, attente, prix, confort, datetime.now().strftime("%d/%m/%Y %H:%M"))
    )
    conn.commit()
    conn.close()

def delete_row(row_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM enquetes WHERE id=?", (row_id,))
    conn.commit()
    conn.close()

init_db()

# ── HEADER ──
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem;">
    <div class="badge">📍 Yaoundé, Cameroun</div>
    <div class="hero-title">Enquête Mobilité Urbaine<br>
    <span class="hero-accent">Yaoundé 2025</span></div>
    <p style="color:#6b7f96; font-size:1rem; margin-top:0.5rem;">
    Collecte de données sur les habitudes de transport des habitants de Yaoundé
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── NAVIGATION ──
tab1, tab2, tab3 = st.tabs(["📋 Nouvelle Enquête", "📊 Données Collectées", "📈 Statistiques"])

# ══════════════════════════════════════
# TAB 1 — FORMULAIRE
# ══════════════════════════════════════
with tab1:
    st.markdown("### 👤 Informations personnelles")
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("Nom complet", placeholder="Ex: Jean Mballa")
    with col2:
        age = st.number_input("Âge (années)", min_value=1, max_value=120, value=25, step=1)

    st.markdown("### 🚗 Mode de transport")
    transport_options = {
        "🚌 Bus": "bus",
        "🚕 Taxi": "taxi",
        "🏍️ Moto-taxi": "moto_taxi",
        "🚗 Voiture personnelle": "voiture_personnelle",
        "🚶 Marche à pied": "marche_a_pied",
        "🔄 Autre": "autre"
    }
    transport_label = st.selectbox("Choisissez le mode de transport", list(transport_options.keys()))
    transport = transport_options[transport_label]

    st.markdown("### ⏱️ Expérience de trajet")
    col3, col4 = st.columns(2)
    with col3:
        attente = st.number_input("Temps d'attente (minutes)", min_value=0, max_value=300, value=10, step=1)
    with col4:
        prix = st.number_input("Prix payé (FCFA)", min_value=0, max_value=100000, value=250, step=50)

    st.markdown("### ⭐ Niveau de confort")
    confort_labels = {
        1: "1 ★ — Très inconfortable",
        2: "2 ★★ — Inconfortable",
        3: "3 ★★★ — Correct",
        4: "4 ★★★★ — Confortable",
        5: "5 ★★★★★ — Très confortable"
    }
    confort = st.select_slider(
        "Notez le confort du trajet",
        options=[1, 2, 3, 4, 5],
        value=3,
        format_func=lambda x: confort_labels[x]
    )

    st.markdown("")
    if st.button("✅ Enregistrer l'enquête"):
        if not nom.strip():
            st.markdown('<div class="error-box">❌ Veuillez entrer un nom</div>', unsafe_allow_html=True)
        else:
            insert(nom.strip(), age, transport, attente, prix, confort)
            st.markdown(f'<div class="success-box">✅ Enquête de <strong>{nom}</strong> enregistrée avec succès !</div>', unsafe_allow_html=True)
            st.balloons()

# ══════════════════════════════════════
# TAB 2 — DONNÉES
# ══════════════════════════════════════
with tab2:
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        filtre = st.selectbox("Filtrer par transport", [
            "Tous", "bus", "taxi", "moto_taxi", "voiture_personnelle", "marche_a_pied", "autre"
        ], format_func=lambda x: {
            "Tous": "🔍 Tous les transports",
            "bus": "🚌 Bus",
            "taxi": "🚕 Taxi",
            "moto_taxi": "🏍️ Moto-taxi",
            "voiture_personnelle": "🚗 Voiture personnelle",
            "marche_a_pied": "🚶 Marche à pied",
            "autre": "🔄 Autre"
        }.get(x, x))

    df = get_all(filtre)

    if df.empty:
        st.info("📭 Aucune donnée disponible. Remplissez le formulaire pour commencer !")
    else:
        st.markdown(f"**{len(df)} enquête(s) trouvée(s)**")

        # Affichage propre
        df_display = df.copy()
        df_display["confort"] = df_display["confort"].apply(lambda x: "★" * x + "☆" * (5-x))
        df_display["prix"] = df_display["prix"].apply(lambda x: f"{int(x):,} FCFA".replace(",", " "))
        df_display["temps_attente"] = df_display["temps_attente"].apply(lambda x: f"{x} min")
        df_display = df_display.rename(columns={
            "id": "ID", "nom": "Nom", "age": "Âge",
            "type_transport": "Transport", "temps_attente": "Attente",
            "prix": "Prix", "confort": "Confort", "date_collecte": "Date"
        })
        st.dataframe(df_display[["ID","Nom","Âge","Transport","Attente","Prix","Confort","Date"]],
                    use_container_width=True, hide_index=True)

        st.markdown("### 🗑️ Supprimer une enquête")
        ids = df["id"].tolist()
        if ids:
            del_id = st.selectbox("Sélectionnez l'ID à supprimer", ids)
            if st.button("🗑️ Supprimer"):
                delete_row(del_id)
                st.success(f"Enquête #{del_id} supprimée !")
                st.rerun()

        st.markdown("### 📥 Télécharger les données")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Télécharger en CSV",
            data=csv,
            file_name="transport_yaounde.csv",
            mime="text/csv"
        )

# ══════════════════════════════════════
# TAB 3 — STATISTIQUES
# ══════════════════════════════════════
with tab3:
    df_all = get_all()

    if df_all.empty:
        st.info("📊 Aucune donnée disponible pour les statistiques.")
    else:
        # Cartes stats globales
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{len(df_all)}</div><div class="stat-label">👥 Enquêtes totales</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{int(df_all["temps_attente"].mean())} min</div><div class="stat-label">⏱️ Attente moyenne</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{int(df_all["prix"].mean()):,} F</div><div class="stat-label">💰 Prix moyen</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stat-box"><div class="stat-value">{df_all["confort"].mean():.1f}/5</div><div class="stat-label">⭐ Confort moyen</div></div>', unsafe_allow_html=True)

        st.markdown("### 📊 Répartition par mode de transport")
        transport_count = df_all["type_transport"].value_counts().reset_index()
        transport_count.columns = ["Transport", "Nombre"]
        st.bar_chart(transport_count.set_index("Transport"))

        st.markdown("### 💰 Prix moyen par transport")
        prix_moy = df_all.groupby("type_transport")["prix"].mean().reset_index()
        prix_moy.columns = ["Transport", "Prix moyen (FCFA)"]
        st.bar_chart(prix_moy.set_index("Transport"))

        st.markdown("### ⭐ Confort moyen par transport")
        confort_moy = df_all.groupby("type_transport")["confort"].mean().reset_index()
        confort_moy.columns = ["Transport", "Confort moyen"]
        st.bar_chart(confort_moy.set_index("Transport"))

        st.markdown("### 📋 Tableau récapitulatif")
        recap = df_all.groupby("type_transport").agg(
            Nombre=("id", "count"),
            Age_moyen=("age", "mean"),
            Attente_moy=("temps_attente", "mean"),
            Prix_moy=("prix", "mean"),
            Confort_moy=("confort", "mean")
        ).round(1).reset_index()
        recap.columns = ["Transport", "Nombre", "Âge moy.", "Attente moy. (min)", "Prix moy. (FCFA)", "Confort moy."]
        st.dataframe(recap, use_container_width=True, hide_index=True)
