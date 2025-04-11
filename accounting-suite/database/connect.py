import os
import oracledb
from dotenv import load_dotenv

# Load environment variables from database/config/db.env
env_path = os.path.join(os.path.dirname(__file__), "config", "db.env")
load_dotenv(env_path)

# Environment config
DB_USER = os.getenv("ORACLE_USER")
DB_PASSWORD = os.getenv("ORACLE_PASS")
CONNECT_STRING = os.getenv("ORACLE_CONNECT_STRING")
WALLET_PATH = os.getenv("ORACLE_WALLET_PATH")
CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH")
USE_THICK_MODE = os.getenv("USE_THICK_MODE", "false").lower() == "true"

# Resolve full paths relative to this file
base_dir = os.path.dirname(__file__)
wallet_full_path = os.path.abspath(os.path.join(base_dir, WALLET_PATH))
client_full_path = os.path.abspath(os.path.join(base_dir, CLIENT_PATH))

# Optional Thick Mode init
if USE_THICK_MODE:
    try:
        oracledb.init_oracle_client(lib_dir=client_full_path)
    except Exception as e:
        print(f"❌ Failed to initialize Oracle Client: {e}")
        raise

def get_oracle_connection():
    try:
        conn = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=CONNECT_STRING,
            config_dir=wallet_full_path,
            wallet_location=wallet_full_path,
            wallet_password=DB_PASSWORD
        )
        return conn
    except oracledb.Error as e:
        print("❌ Oracle connection failed:", e)
        raise

if __name__ == "__main__":
    try:
        conn = get_oracle_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT current_date FROM dual")
            print("✅ Connected. DB date is:", cur.fetchone()[0])
    finally:
        if conn:
            conn.close()

