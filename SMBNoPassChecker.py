#!/usr/bin/env python3

import argparse
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

def save_output(output_file, content):
    """
    Save the given content to the specified output file.
    """
    try:
        with open(output_file, 'a') as file:
            file.write(f'{content}\n')
    except Exception as e:
        print(f"[Error] Could not save output: {e}")

def check_smb_access(server, share, user, output_file, verbose):
    """
    Check SMB access using smbclient and no password for the given user.
    """
    try:
        command = [
            "smbclient",
            f"//{server}/{share}",
            "-U", user,
            "-N",
            "-c", "exit"
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            message = f"[SUCCESS] User '{user}' has no-password access to share '{share}' on server '{server}'"
            save_output(output_file, message)
            if verbose:
                print(message)
        else:
            message = f"[FAIL] User '{user}' cannot access share '{share}' on server '{server}': {result.stderr.strip()}"
            if verbose:
                print(message)

    except FileNotFoundError:
        print("[Error] 'smbclient' is not installed or not in the PATH.\n")

    except Exception as e:
        print(f"[Error] Failed to check access: {e}")

def main():

    parser = argparse.ArgumentParser(description="SMBNoPassChecker is a simple Python script to check SMB shares for accessible resources without requiring a password. Supports customizable options using argument parsing for flexibility and ease of use.")
    parser.add_argument(
        '-s',
        '--server',
        required=True,
        type=str,
        help="Enter the SMB server IP/Host address (e.g., 192.168.1.10)",
    )

    parser.add_argument(
        '-uL',
        '--users-list',
        required=True,
        type=str,
        help="Enter the path to the SMB users file",
    )

    parser.add_argument(
        '-sL',
        '--shares-list',
        required=True,
        type=str,
        help="Enter the path to the SMB shares file",
    )

    parser.add_argument(
        '-o',
        '--output',
        default='SMBNoPassOutput.txt',
        type=str,
        help="Enter your output file",
    )

    parser.add_argument(
        '-v',
        '--verbose',
        required=False,
        action='store_true',
        help="Enable verbose mode",
    )

    args = parser.parse_args()
    server = args.server
    users_file = args.users_list
    shares_file = args.shares_list

    users = load_file(users_file)
    shares = load_file(shares_file)

    if not users or not shares:
        print("[Error] Ensure both files are correctly specified and non-empty.")
        return

    print(f"\n[INFO] Testing SMB access on server '{server}' with {len(users)} users and {len(shares)} shares, Please wait...\n")

    for user in users:
        for share in shares:
            check_smb_access(server, share, user, args.output, args.verbose)

    print(f'\n[INFO] Check results on: {args.output}')

if __name__ == "__main__":
    main()

