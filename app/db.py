# File Helper
import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "db_docker")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

## Buat koneksi ke database
def get_connection():
    conn = psycopg2.connect(
        host= DB_HOST,
        port= DB_PORT,
        dbname= DB_NAME,
        user = DB_USER,
        password= DB_PASSWORD
    )
    return conn

## Contoh query SELECT
def get_all_customers():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT id, name, email, is_active, created_at FROM customers ORDER BY id;")
            rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

## Contoh query INSERT
def create_customer(name, email):
    conn = get_connection()
    try: 
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO customers (name,email)
                VALUES (%s, %s)
                RETURNING id, name, email, is_active, created_at;
                """,
                (name, email)
            )
            new_row = cursor.fetchone()
        conn.commit()
        return new_row
    finally:
        conn.close()

        