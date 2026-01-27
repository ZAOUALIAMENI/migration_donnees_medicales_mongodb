import os
import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus

# =========================================================
# Fonction 1 : Connexion aux ressources
# =========================================================
def connect_resources(csv_file, collection_name="patients"):
    """
    Connexion sécurisée au fichier CSV et à MongoDB
    via des variables d’environnement.
    """
    # Chargement du CSV
    df = pd.read_csv(csv_file)

    # Variables d’environnement MongoDB
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")
    db_name = os.getenv("MONGO_DB")

    # Encodage du mot de passe
    password = quote_plus(password)

    uri = (
        f"mongodb://{user}:{password}@{host}:{port}/{db_name}"
        f"?authSource={db_name}&authMechanism=SCRAM-SHA-256"
    )

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    print("Connexion MongoDB sécurisée et chargement CSV OK")
    return df, client, collection

# =========================================================
# Test 1 : Nombre de lignes CSV vs MongoDB
# =========================================================
def test_row_count(df, collection):
    """
    Vérifie que le nombre de lignes CSV correspond au nombre
    de documents MongoDB.
    """
    csv_count = len(df)
    mongo_count = collection.count_documents({})

    print("\nTEST 1 — Nombre de lignes")
    print(f"Lignes CSV        : {csv_count}")
    print(f"Documents MongoDB : {mongo_count}")

    if csv_count == mongo_count:
        print("OK : le nombre correspond")
    else:
        print("ATTENTION : différence détectée")


# =========================================================
# Test 2 : Colonnes disponibles dans le CSV
# =========================================================
def test_csv_columns(df):
    """
    Vérifie la présence des colonnes attendues dans le CSV.
    """
    expected_columns = [
        "Name", "Age", "Gender", "Blood Type", "Medical Condition",
        "Date of Admission", "Doctor", "Hospital",
        "Insurance Provider", "Billing Amount", "Room Number",
        "Admission Type", "Discharge Date", "Medication", "Test Results"
    ]

    print("\nTEST 2 — Colonnes du CSV")

    missing = set(expected_columns) - set(df.columns)

    if not missing:
        print("OK : toutes les colonnes sont présentes")
    else:
        print("Colonnes manquantes :", missing)


# =========================================================
# Test 3 : Valeurs manquantes dans le CSV
# =========================================================
def test_missing_values_csv(df):
    """
    Vérifie les valeurs manquantes dans le fichier CSV.
    """
    print("\nTEST 3 — Valeurs manquantes (CSV)")
    missing = df.isnull().sum()
    print(missing)

    if missing.sum() == 0:
        print("OK : aucune valeur manquante dans le CSV")
    else:
        print("ATTENTION : valeurs manquantes détectées")


# =========================================================
# Test 4 : Valeurs manquantes dans MongoDB
# =========================================================
def test_missing_values_mongo(collection):
    """
    Vérifie la présence des champs essentiels dans MongoDB.
    """
    print("\nTEST 4 — Valeurs manquantes (MongoDB)")

    required_fields = [
        "name", "age", "gender", "blood_type",
        "medical_condition", "billing_amount", "admission"
    ]

    missing_fields = False

    for field in required_fields:
        count = collection.count_documents({field: {"$exists": False}})
        print(f"{field} manquant : {count}")
        if count > 0:
            missing_fields = True

    if not missing_fields:
        print("OK : champs essentiels présents")
    else:
        print("ATTENTION : champs manquants détectés")


# =========================================================
# Test 5 : Doublons (name + admission.date)
# =========================================================
def test_duplicates(collection):
    """
    Détecte les doublons potentiels basés sur name et admission.date.
    """
    print("\nTEST 5 — Doublons potentiels (name + admission.date)")

    pipeline = [
        {
            "$group": {
                "_id": {
                    "name": "$name",
                    "date": "$admission.date"
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {"count": {"$gt": 1}}
        }
    ]

    duplicates = list(collection.aggregate(pipeline))
    print(f"Doublons détectés : {len(duplicates)}")

    if len(duplicates) == 0:
        print("OK : aucun doublon détecté")
    else:
        print("ATTENTION : doublons métier possibles")


# =========================================================
# Test 6 : Types de toutes les variables (échantillon)
# =========================================================
def test_field_types(collection):
    """
    Vérifie les types des champs sur un document échantillon.
    """
    print("\nTEST 6 — Types des champs (échantillon)")

    sample = collection.find_one()

    expected_types = {
        "name": str,
        "age": int,
        "gender": str,
        "blood_type": str,
        "medical_condition": str,
        "medication": str,
        "test_results": str,
        "billing_amount": float,
        "admission": dict
    }

    for field, expected_type in expected_types.items():
        if isinstance(sample.get(field), expected_type):
            print(f"{field} : type correct")
        else:
            print(f"{field} : type incorrect")


# =========================================================
# Fonction principale
# =========================================================
def main():
    csv_file = "healthcare_dataset.csv"

    df, client, collection = connect_resources(csv_file)

    test_row_count(df, collection)
    test_csv_columns(df)
    test_missing_values_csv(df)
    test_missing_values_mongo(collection)
    test_duplicates(collection)
    test_field_types(collection)

    client.close()
    print("\nTests d’intégrité terminés")


# =========================================================
# Point d’entrée
# =========================================================
if __name__ == "__main__":
    main()
