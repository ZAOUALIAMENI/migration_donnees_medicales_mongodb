// Sélection de la base
db = db.getSiblingDB("medical_db");

// =====================
// Admin
// =====================
db.createUser({
  user: "admin_medical",
  pwd: "Admin123.",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "dbAdmin", db: "medical_db" },
    { role: "readWrite", db: "medical_db" }
  ]
});

// =====================
// Writer
// =====================
db.createUser({
  user: "writer_medical",
  pwd: "Writer123.",
  roles: [
    { role: "readWrite", db: "medical_db" }
  ]
});

// =====================
// Reader
// =====================
db.createUser({
  user: "reader_medical",
  pwd: "Reader123.",
  roles: [
    { role: "read", db: "medical_db" }
  ]
});

print("✔ Utilisateurs MongoDB créés avec succès");
