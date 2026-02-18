# migration_donnees_medicales_mongodb

## Contexte
Dans le cadre d’une mission Data Engineer chez DataSoluTech, l’objectif est de migrer un dataset de données médicales au format CSV vers une base MongoDB scalable, sécurisée et conteneurisée avec Docker.
Le client rencontre des problèmes de performance liés à la croissance des données.
Une solution NoSQL orientée Big Data est donc mise en place.

## Objectifs
- Migrer les données CSV vers MongoDB
- Mettre en place une architecture Docker reproductible
- Sécuriser les accès via gestion des rôles
- Mettre en œuvre des tests d’intégrité et tests unitaires
-Préparer une architecture évolutive vers le cloud (AWS)

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
## Workflow
1) Lecture du fichier CSV
2) Transformation des données
3) Connexion sécurisée à MongoDB
4) Insertion des documents
5) Persistance dans le volume Docker
6) Exécution des tests
## Résultats
- 55 500 lignes CSV migrées vers MongoDB
- Modèle NoSQL validé
- Tests d’intégrité réussis

## Architecture Dockeer
### Services
- Service MongoDB
Image : mongo:7
Volume : mongo_data
Script d’initialisation : mongo-init.js
Réseau : medical_network
- Service application
Build local (Dockerfile)
Exécution du script de migration
Lecture des variables depuis .env
### Volumes
mongo_data: permet la concervation des données même après la suppression du conteneur
### Network
medical_network (bridge) : permet la communication sécurisée entre les conteneurs

## Sécurité 
Les utilisateurs MongoDB sont créés automatiquement via le script d'initialisation Docker : docker/mongo-int.js
admin_medical → rôle admin
writer_medical → rôle readWrite
reader_medical → rôle read
L'application utilise seulement l'utilisateur writer_medical

Sécurité et authentification
- L’application Python ne se connecte jamais avec un compte administrateur
- Les identifiants MongoDB sont stockés dans des variables d’environnement
- Aucune information sensible (mot de passe) n’est présente dans le code source
Exemple de variables utilisées :
- `MONGO_USER`
- `MONGO_PASSWORD`
- `MONGO_HOST`
- `MONGO_PORT`
- `MONGO_DB`
Les identifiant sont stocké dans un fichier .env et le fichier est excl de versioning via .gitignore
## Tests 
1) Tests d’intégrité des données (data_integrity_check.py)
Vérifications :
- Nombre de lignes vs MongoDB
- Colonnes disponibles
- Valeurs manquantes
- Les doublons
- Types
Exécution avec : python data-integrity_check.py
2) Tests unitaires (test_unit_mongodb.py)
  Vérifications :
  - Connexion Mongo
  - Présence des colonnes attendues dans csv (Name, age…)
  - Longueur des lignes positive dans le csv
  - Nombre de lignes CSV correspond aux documents MongoDB
  - Structure d’un document patient
  - Champs manquants
  - Age positive
  - Valeur de la facturation positive
  - Le genre (male, femelle, autre)
  - Le groupe sanguins (A+, A-, B+ …)
  - Un patient doit avoir une date et un type d'admission

## Modélisation MongoDB
Collection principale : patients
Structure d'un document : schema_mongodb.json
## Choix techniques
### MongoDB
- Adapté aux données évolutives
- Scalabilité horizontale (sharding)
- Modèle document adapté aux données médicales
### Docker 
- Reproductibilité
- Isolations des services
- Préparation au cloud
### Gestion des roles
- Sécurité
- Séparation des responsabilités
### Tests
- Vérification de la qualité des données
- détercter les anomalies automatiquement

## Perspective Cloud (AWS) 
Architecture compatible avec :
- Amazon DocumentDB
- Amazon ECS
- Amazon S3
- Amazon EC2
La conteneurisation facilite le déploiement vers le cloud.

## Installation et exécution 
1) Cloner le repository
   git clone <https://github.com/ZAOUALIAMENI/migration_donnees_medicales_mongodb/tree/main>
   cd projet_mongodb
   
2) Créer le fichier .env à la racine du projet
   MONGO_USER=writer_medical
   MONGO_PASSWORD=...
   MONGO_HOST=mongo
   MONGO_PORT=27017
   MONGO_DB=medical_db

3) Lancer Docker : 
- docker compose up --build : La migration s'exécute automatiquement
- docker compose ps : vérification des conteneurs

4) Lancer les tests 
- python data_integrity_check.py : tests d'intégrité
- pytest : tests unitaires

