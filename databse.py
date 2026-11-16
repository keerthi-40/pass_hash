#database module for password vault
import sqlite3

import os

from security import ph

DB_NAME = "vault.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                master_hash TEXT,
                salt BLOB
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS secrets (
                site TEXT,
                username TEXT,
                encrypted_password TEXT
            )
        """)

        conn.commit()


def setup_account():
    from getpass import getpass

    print("--- Initialize Your Vault ---")

    mp = getpass("Create a Master Password: ")
    confirm = getpass("Confirm Master Password: ")

    if mp != confirm:
        print("Passwords do not match!")
        return

    salt = os.urandom(16)
    master_hash = ph.hash(mp)

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO config VALUES (?, ?)",
            (master_hash, salt)
        )

    print("Vault initialized successfully.")


def get_vault_config():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute(
            "SELECT master_hash, salt FROM config"
        ).fetchone()