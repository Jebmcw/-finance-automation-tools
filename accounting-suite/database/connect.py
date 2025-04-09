import os
import oracledb
from dotenv import load_dotenv

# Load .env from database/config/db.env
env_path = os.path.join(os.path.dirname(__file__), "config", "db.env")
load_dotenv(env_path)

# Load config values
DB_USER = os.getenv("ORACLE_USER")
DB_PASSWORD = os.getenv("ORACLE_PASS")
CONNECT_STRING = os.getenv("ORACLE_CONNECT_STRING")
WALLET_PATH = os.getenv("ORACLE_WALLET_PATH")
CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH")

# Resolve full paths
base_dir = os.path.dirname(__file__)
wallet_full_path = os.path.join(base_dir, WALLET_PATH)
client_full_path = os.path.join(base_dir, CLIENT_PATH)

# Optional: enable Thick mode fallback
USE_THICK_MODE = False  # Set to True if you want to force thick mode

# Initialize Oracle Client for Thick mode only if needed
if USE_THICK_MODE:
    oracledb.init_oracle_client(lib_dir=client_full_path)

def get_oracle_connection():
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=CONNECT_STRING,
        config_dir=wallet_full_path,
        wallet_location=wallet_full_path,
        wallet_password=DB_PASSWORD  # default for ATP wallet
    )
    return conn

if __name__ == "__main__":
    conn = get_oracle_connection()
    cur = conn.cursor()
    cur.execute("SELECT current_date FROM dual")
    print("✅ Connected. DB date is:", cur.fetchone()[0])
    cur.close()
    conn.close()
