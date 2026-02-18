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
- `data_integrity_check.py` : tests d’intégrité
- `test_unit_mongodb.py` : tests unitaires
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

## Gestion des utilisateurs MongoDB et sécurité
La base de données MongoDB utilise une gestion par rôles afin de garantir
la sécurité et le principe du moindre privilège.
### Utilisateurs créés
Les utilisateurs sont créés automatiquement au démarrage de MongoDB
via un script d’initialisation Docker.

| Utilisateur        | Rôle(s) attribué(s)            | Description |
|--------------------|--------------------------------|------------|
| admin_medical      | admin / dbAdmin / readWrite    | Administration complète de la base |
| writer_medical     | readWrite                      | Insertion et modification des données |
| reader_medical     | read                            | Consultation des données uniquement |

### Sécurité et authentification
- L’application Python ne se connecte jamais avec un compte administrateur
- Les identifiants MongoDB sont stockés dans des variables d’environnement
- Aucune information sensible (mot de passe) n’est présente dans le code source
Exemple de variables utilisées :
- `MONGO_USER`
- `MONGO_PASSWORD`
- `MONGO_HOST`
- `MONGO_PORT`
- `MONGO_DB`

## Tests unitaires automatisés (pytest)
Les tests unitaires sont exécutés avec `pytest` et permettent de vérifier :
- la cohérence entre le CSV et MongoDB ;
- la structure des documents ;
- les types des champs ;
- certaines règles de qualité des données (valeurs positives, catégories valides).

## Déploiement avec Docker
Le projet est entièrement conteneurisé à l’aide de Docker.
Un script d’initialisation est exécuté automatiquement au premier démarrage :
- création de la base `medical_db`
- création des utilisateurs :
  - admin_medical
  - writer_medical
  - reader_medical
- attribution des rôles (read, readWrite, admin)
- lancement : docker compose up --build





