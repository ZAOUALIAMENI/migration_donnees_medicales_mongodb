# migration_donnees_medicales_mongodb
## Contexte
Ce projet consiste à migrer un jeu de données médicales stocké dans un fichier CSV vers une base de données MongoDB, dans le cadre d’une mission de Data Engineer.
## Objectifs
- Migrer automatiquement les données CSV vers MongoDB
- Concevoir un modèle NoSQL adapté
- Tester l’intégrité et la qualité des données
- Mettre en place des tests unitaires
- Documenter l’ensemble de la démarche
## Technologies utilisées
- Python
- MongoDB Compass
- Pandas
- PyMongo
- Pytest
- GitHub
## Structure du projet
- `migrate_csv_to_mongo.py` : script de migration
- `test_data_integrity.py` : tests d’intégrité
- `test_unit_patients.py` : tests unitaires
- `healthcare_dataset.csv` : données source
- `schema_mongodb.json` : schéma de la base
## Résultats
- 55 500 lignes CSV migrées vers MongoDB
- Modèle NoSQL validé
- Tests d’intégrité réussis
## Sécurité
La connexion à MongoDB repose sur des utilisateurs et rôles distincts
(admin, writer, reader). Les identifiants sont stockés dans des variables
d’environnement afin d’éviter toute exposition de données sensibles.
