# TransportData Yaoundé 🚌

Application de collecte de données sur les transports urbains à Yaoundé.

## Structure

```
transport-yaounde/
├── backend/
│   ├── app.py           ← API Flask (Python)
│   └── requirements.txt
└── frontend/
    └── index.html       ← Interface utilisateur
```

## Lancement

### 1. Backend Python
```bash
cd backend
pip install -r requirements.txt
python app.py
```
→ API disponible sur http://localhost:5000

### 2. Frontend
Ouvrir `frontend/index.html` dans un navigateur.

## Endpoints API

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | /api/health | Statut de l'API |
| POST | /api/enquetes | Créer une enquête |
| GET | /api/enquetes | Lister les enquêtes |
| GET | /api/enquetes?transport=taxi | Filtrer par transport |
| DELETE | /api/enquetes/:id | Supprimer une enquête |
| GET | /api/statistiques | Statistiques globales |

## Données collectées
- **Nom** – Nom du participant
- **Âge** – Âge en années
- **Type de transport** – bus, taxi, moto_taxi, voiture_personnelle, marche_a_pied, autre
- **Temps d'attente** – En minutes
- **Prix** – En FCFA
- **Confort** – Note de 1 à 5
