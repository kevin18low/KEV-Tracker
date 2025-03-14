import express from "express";
import bodyParser from "body-parser";
import mysql2 from "mysql2/promise";
import env from "dotenv";
import crypto from "crypto";

const app = express();
const PORT = 4000;
app.use(bodyParser.json());
env.config();

let db;

// Async connection establishment
const connectDB = async () => {
  try {
    db = await mysql2.createConnection({
      host: process.env.INTERNAL_HOST,
      user: process.env.USER,
      password: process.env.PW,
      database: process.env.DB,
    });
    console.log('Database connected successfully');
    await createApiKeyTable();
  } catch (error) {
    console.error('Database connection failed:', error);
    process.exit(1);
  }
};

// Create API keys table if it doesn't exist
const createApiKeyTable = async () => {
  try {
    await db.execute(`
      CREATE TABLE IF NOT EXISTS api_keys (
      id INT AUTO_INCREMENT PRIMARY KEY,
      api_key VARCHAR(64) NOT NULL UNIQUE,
      user_id INT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      last_used TIMESTAMP NULL,
      is_active BOOLEAN DEFAULT TRUE
      )
    `);
  } catch (error) {
    console.error('Error creating API keys table:', error);
  }
};

// Verify API key
const verifyApiKey = async (req, res, next) => {
  const apiKey = req.header('x-api-key') || req.query.api_key;
  const userId = req.header('user-id') || req.query.user_id || req.body.user_id;
  
  if (!apiKey) {
    return res.status(401).json({ error: 'API key is required' });
  }

  if (!userId) {
    return res.status(401).json({ error: 'userID is required' });
  }
  
  try {
    const [rows] = await db.execute(
      'SELECT * FROM api_keys WHERE api_key = ? AND is_active = TRUE AND user_id = ?',
      [apiKey, userId]
    );
    
    if (rows.length === 0) {
      return res.status(401).json({ error: 'Invalid API key' });
    }
        
    // Update last_used timestamp
    await db.execute(
      'UPDATE api_keys SET last_used = CURRENT_TIMESTAMP WHERE api_key = ? AND user_id = ?',
      [apiKey, userId]
    );
    
    req.apiKeyInfo = rows[0];
    next();
  } catch (error) {
    return res.status(500).json({ error: 'Failed to authenticate API key' });
  }
};

// Generate a new API key
const generateApiKey = () => {
  return crypto.randomBytes(32).toString('hex');
};

// Initialize connection before starting server
const startServer = async () => {
    await connectDB();
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
};
  
startServer();

// Create new API key
app.post("/api-keys", async (req, res) => {
  try {
    const user_id = req.headers['user-id'];
    
    const apiKey = generateApiKey();
    
    await db.execute(
      'INSERT INTO api_keys (api_key, user_id) VALUES (?, ?)',
      [apiKey, user_id]
    );
    
    res.status(201).json({ 
      user_id: user_id,
      apiKey 
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get all cveIDs from database
app.get("/cve", verifyApiKey, async (req, res) => {
  try {
    const [rows] = await db.execute("SELECT cveID FROM KEV_Catalog");
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get all records from KEV database
app.get("/", verifyApiKey, async (req, res) => {
  try {
    const [rows] = await db.execute("SELECT * FROM KEV_Catalog");
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get number of records in database
app.get("/count", verifyApiKey, async (req, res) => {
    try {
      const [rows] = await db.execute("SELECT COUNT(cveID) FROM KEV_Catalog");
      res.json(rows);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
});

// Get record by cveID
app.get("/cve/:cveID", verifyApiKey, async (req, res) => {
    try {
      const [rows] = await db.execute("SELECT * FROM KEV_Catalog WHERE cveID = ?", [req.params.cveID]);
      res.json(rows);
    } catch (err) {
      res.status(500).json({ error: err.message });
    }
});

// Get all records from a specific vendor
app.get("/:vendor", verifyApiKey, async (req, res) => {
  try {
    const [rows] = await db.execute("SELECT * FROM KEV_Catalog WHERE LOWER(vendorProject) = LOWER(?)", [req.params.vendor]);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


