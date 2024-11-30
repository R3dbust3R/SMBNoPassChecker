#!/usr/bin/env python3


import subprocess

def load_file(file_path):
    """
    Load content from a file and return as a list of lines.
    """
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[Error] File '{file_path}' not found.")
        return []

def check_smb_access(server, share, user):
    """
    Check SMB access using smbclient and no password for the given user.
    """
    try:
        # Build the smbclient command
        command = [
            "smbclient",
            f"//{server}/{share}",
            "-U", user,  # Username
            "-N",        # No password flag
            "-c", "exit" # Command to run (exit after checking access)
        ]
        # Execute the command and capture output
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print(f"[SUCCESS] User '{user}' has no-password access to share '{share}' on server '{server}'")
        else:
            print(f"[FAIL] User '{user}' cannot access share '{share}' on server '{server}': {result.stderr.strip()}")
    except Exception as e:
        print(f"[Error] Failed to run smbclient: {e}")

def main():
    server = input("Enter the SMB server address (e.g., 192.168.1.10): ").strip()
    users_file = input("Enter the path to the SMB users file: ").strip()
    shares_file = input("Enter the path to the SMB shares file: ").strip()

    users = load_file(users_file)
    shares = load_file(shares_file)

    if not users or not shares:
        print("[Error] Ensure both files are correctly specified and non-empty.")
        return

    print(f"\n[Info] Testing SMB access on server '{server}' with {len(users)} users and {len(shares)} shares...\n")
    for user in users:
        for share in shares:
            check_smb_access(server, share, user)

if __name__ == "__main__":
    main()

