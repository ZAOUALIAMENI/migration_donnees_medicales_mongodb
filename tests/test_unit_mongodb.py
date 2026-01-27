import os
import pandas as pd
import pytest
from pymongo import MongoClient
from urllib.parse import quote_plus

# =========================
# Fixtures pytest
# =========================

@pytest.fixture(scope="module")
def csv_dataframe():
    """Charge le fichier CSV une seule fois."""
    return pd.read_csv("healthcare_dataset.csv")


@pytest.fixture(scope="module")
def mongo_collection():
    """Connexion sécurisée à MongoDB."""
    user = os.getenv("MONGO_USER")
    password = quote_plus(os.getenv("MONGO_PASSWORD"))
    host = os.getenv("MONGO_HOST")
    port = os.getenv("MONGO_PORT")
    db_name = os.getenv("MONGO_DB")

    uri = (
        f"mongodb://{user}:{password}@{host}:{port}/{db_name}"
        f"?authSource={db_name}&authMechanism=SCRAM-SHA-256"
    )

    client = MongoClient(uri)
    collection = client[db_name]["patients"]

    yield collection
    client.close()

# =========================
# Tests unitaires
# =========================

def test_csv_loaded(csv_dataframe):
    """Le CSV doit contenir des lignes."""
    assert len(csv_dataframe) > 0


def test_csv_columns(csv_dataframe):
    """Vérifie la présence des colonnes attendues."""
    expected_columns = {
        "Name", "Age", "Gender", "Blood Type", "Medical Condition",
        "Date of Admission", "Doctor", "Hospital",
        "Insurance Provider", "Billing Amount", "Room Number",
        "Admission Type", "Discharge Date", "Medication", "Test Results"
    }

    assert expected_columns.issubset(set(csv_dataframe.columns))


def test_mongo_connection(mongo_collection):
    """La collection MongoDB doit être accessible."""
    assert mongo_collection is not None


def test_row_count_match(csv_dataframe, mongo_collection):
    """Le nombre de lignes CSV doit correspondre aux documents MongoDB."""
    assert len(csv_dataframe) == mongo_collection.count_documents({})


def test_sample_document_structure(mongo_collection):
    """Vérifie la structure d'un document patient."""
    doc = mongo_collection.find_one()

    assert isinstance(doc["name"], str)
    assert isinstance(doc["age"], int)
    assert isinstance(doc["billing_amount"], float)
    assert isinstance(doc["admission"], dict)


def test_no_missing_essential_fields(mongo_collection):
    """Aucun champ essentiel ne doit être manquant."""
    required_fields = [
        "name", "age", "gender", "blood_type",
        "medical_condition", "billing_amount", "admission"
    ]

    for field in required_fields:
        missing = mongo_collection.count_documents({field: {"$exists": False}})
        assert missing == 0

def test_age_positive(mongo_collection):
    """L'âge doit être positif."""
    sample = mongo_collection.find({"age": {"$exists": True}}).limit(100)

    for doc in sample:
        assert doc["age"] >= 0


def test_billing_amount_positive(mongo_collection):
    """Le montant de facturation doit être positif."""
    sample = mongo_collection.find({"billing_amount": {"$exists": True}}).limit(100)

    for doc in sample:
        assert doc["billing_amount"] >= 0


def test_gender_values(mongo_collection):
    """Les valeurs de genre doivent être connues."""
    allowed = {"Male", "Female", "Other"}
    sample = mongo_collection.find({"gender": {"$exists": True}}).limit(100)

    for doc in sample:
        assert doc["gender"] in allowed


def test_blood_type_values(mongo_collection):
    """Les groupes sanguins doivent être valides."""
    allowed = {"A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"}
    sample = mongo_collection.find({"blood_type": {"$exists": True}}).limit(100)

    for doc in sample:
        assert doc["blood_type"] in allowed


def test_admission_has_date_and_type(mongo_collection):
    """Un patient doit avoir une date et un type d'admission."""
    sample = mongo_collection.find({"admission": {"$exists": True}}).limit(100)

    for doc in sample:
        admission = doc["admission"]
        assert "date" in admission
        assert "type" in admission
        assert admission["date"] is not None
        assert admission["type"] is not None
