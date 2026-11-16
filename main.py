from getpass import getpass

from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet

from security import ph, derive_key
from database import init_db, setup_account, get_vault_config
from vault_operations import add_password, list_passwords


def main():

    init_db()
    config = get_vault_config()

    if not config:
        setup_account()
        return

    stored_hash, salt = config

    master_pwd = getpass("Enter Master Password: ")

    try:
        ph.verify(stored_hash, master_pwd)
        print("Access Granted.")

    except VerifyMismatchError:
        print("Access Denied: Incorrect Password.")
        return

    key = derive_key(master_pwd, salt)
    fernet = Fernet(key)

    while True:

        print("\n1. Add Password")
        print("2. View Passwords")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            add_password(fernet)

        elif choice == "2":
            list_passwords(fernet)

        elif choice == "3":
            print("Exiting Password Vault...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()