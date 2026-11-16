import sqlite3
from getpass import getpass

from database import DB_NAME


def add_password(fernet):

    site = input("Enter Website: ")
    user = input("Enter Username: ")
    pwd = getpass("Enter Password to Save: ")

    encrypted = fernet.encrypt(pwd.encode()).decode()

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO secrets VALUES (?, ?, ?)",
            (site, user, encrypted)
        )

    print(f"Stored credentials for {site}!")


def list_passwords(fernet):

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute(
            "SELECT site, username, encrypted_password FROM secrets"
        ).fetchall()

    if not rows:
        print("No passwords saved yet.")
        return

    print("\n--- Your Saved Passwords ---")

    for site, user, enc_pwd in rows:
        try:
            decrypted = fernet.decrypt(
                enc_pwd.encode()
            ).decode()

            print(
                f"Site: {site:15} | "
                f"User: {user:15} | "
                f"Password: {decrypted}"
            )

        except Exception:
            print(f"Error decrypting {site}")