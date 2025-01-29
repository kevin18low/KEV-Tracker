import express from "express";
import bodyParser from "body-parser";
import mysql2 from "mysql2/promise";
import env from "dotenv";

const app = express();
const PORT = 4000;
app.use(bodyParser.json());
env.config();

let db;

// Async connection establishment
const connectDB = async () => {
  try {
    db = await mysql2.createConnection({
      host: process.env.HOST,
      user: process.env.USER,
      password: process.env.PW,
      database: process.env.DB,
    });
    console.log('Database connected successfully');
  } catch (error) {
    console.error('Database connection failed:', error);
    process.exit(1);
  }
};

// Initialize connection before starting server
const startServer = async () => {
    await connectDB();
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
};
  
startServer();

// Get all cveIDs from database
app.get("/cve", async (req, res) => {
  try {
    const [rows] = await db.execute("SELECT cveID FROM KEV_Catalog");
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get all records from KEV database
app.get("/", async (req, res) => {
  try {
    const [rows] = await db.execute("SELECT * FROM KEV_Catalog");
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get number of records in database
app.get("/count", async (req, res) => {
    try {
      const [rows] = await db.execute("SELECT COUNT(cveID) FROM KEV_Catalog");
      res.json(rows);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
});

// Get record by cveID
app.get("/cve/:cveID", async (req, res) => {
    try {
      const [rows] = await db.execute("SELECT * FROM KEV_Catalog WHERE cveID = ?", [req.params.cveID]);
      res.json(rows);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
});

// Get all records from a specific vendor
app.get("/:vendor", async (req, res) => {
  try {
    const [rows] = await db.execute("SELECT * FROM KEV_Catalog WHERE LOWER(vendorProject) = LOWER(?)", [req.params.vendor]);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


