import pandas as pd
from pymongo import MongoClient

# =========================================================
# Fonction 1 : Connexion à MongoDB
# =========================================================
def connect_to_mongodb(uri="mongodb://localhost:27017",
                       db_name="medical_db",
                       collection_name="patients"):
    """
    Établit une connexion à MongoDB et retourne la collection cible.
    """
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    print("Connexion à MongoDB réussie")
    return client, collection


# =========================================================
# Fonction 2 : Lecture du fichier CSV
# =========================================================
def load_csv(csv_file):
    """
    Charge le fichier CSV dans un DataFrame pandas.
    """
    df = pd.read_csv(csv_file)
    print("Colonnes du CSV :")
    print(df.columns)
    print(f"Nombre de lignes dans le CSV : {len(df)}")
    return df


# =========================================================
# Fonction 3 : Transformation d'une ligne CSV en document MongoDB
# =========================================================
def build_patient_document(row):
    """
    Transforme une ligne du CSV en document MongoDB conforme au modèle.
    """
    patient = {
        "name": row["Name"],
        "age": int(row["Age"]),
        "gender": row["Gender"],
        "blood_type": row["Blood Type"],

        "medical_condition": row["Medical Condition"],
        "medication": row["Medication"],
        "test_results": row["Test Results"],

        "admission": {
            "date": row["Date of Admission"],
            "type": row["Admission Type"],
            "doctor": row["Doctor"],
            "hospital": row["Hospital"],
            "room_number": int(row["Room Number"])
        },

        "discharge_date": row["Discharge Date"],
        "insurance_provider": row["Insurance Provider"],
        "billing_amount": float(row["Billing Amount"])
    }
    return patient


# =========================================================
# Fonction 4 : Insertion des données dans MongoDB
# =========================================================
def insert_patients(df, collection):
    """
    Insère les patients ligne par ligne dans MongoDB.
    """
    inserted_count = 0

    for _, row in df.iterrows():
        patient = build_patient_document(row)
        collection.insert_one(patient)
        inserted_count += 1

    print(f"{inserted_count} documents insérés avec succès")


# =========================================================
# Fonction principale (point d'entrée du script)
# =========================================================
def main():
    """
    Fonction principale orchestrant la migration CSV -> MongoDB.
    """
    csv_file = "healthcare_dataset.csv"

    # Connexion MongoDB
    client, collection = connect_to_mongodb()

    # Chargement du CSV
    df = load_csv(csv_file)

    # Insertion des données
    insert_patients(df, collection)

    # Fermeture de la connexion
    client.close()
    print("Migration terminée")


# =========================================================
# Lancement du script
# =========================================================
if __name__ == "__main__":
    main()
