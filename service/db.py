import psycopg2
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5433")),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "postgres"),
    "dbname": os.getenv("DB_NAME", "postgres"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)
