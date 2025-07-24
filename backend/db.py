import os
from dotenv import load_dotenv
import aiomysql
from passlib.context import CryptContext

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Pranusha@278992")
MYSQL_DB = os.getenv("MYSQL_DB", "supplywhiz")
JWT_SECRET = os.getenv("JWT_SECRET", "SECRET")

print("DEBUG: MYSQL_USER =", MYSQL_USER)
print("DEBUG: MYSQL_PASSWORD =", MYSQL_PASSWORD)
print("DEBUG: MYSQL_DB =", MYSQL_DB)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_mysql_pool():
    return await aiomysql.create_pool(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        autocommit=True
    )