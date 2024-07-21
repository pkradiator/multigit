import subprocess
import os
import json

CONFIG_FILE = 'git_accounts.json'


def check_shell():
    try:
        shell = os.environ['SHELL']
    except :
        print("$SHELL evironment variable could not be found\nCannot Automatically detect shell (termianl).")



def load_accounts():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_accounts(accounts):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(accounts, file, indent=4)

def start_ssh_agent():
    try:
        agent_info = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True, check=True)
        for line in agent_info.stdout.splitlines():
            if line.startswith('SSH_AUTH_SOCK'):
                sock_line = line.split(';')[0]
                os.environ['SSH_AUTH_SOCK'] = sock_line.split('=')[1]
            elif line.startswith('SSH_AGENT_PID'):
                pid_line = line.split(';')[0]
                os.environ['SSH_AGENT_PID'] = pid_line.split('=')[1]
        print("Started ssh-agent.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Failed to start ssh-agent.")

def switch_git_account(name, email, ssh_key_path):
    try:
        # Set the user name
        subprocess.run(['git', 'config', '--global', 'user.name', name], check=True)

        # Set the user email
        subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)

        print(f"Switched Git account to: {name} <{email}>")

        # Start the ssh-agent
        start_ssh_agent()

        # Remove all keys from the ssh-agent
        subprocess.run(['ssh-add', '-D'], check=True)

        # Add the new SSH key to the ssh-agent
        subprocess.run(['ssh-add', ssh_key_path], check=True)

        # List keys to confirm
        subprocess.run(['ssh-add', '-l'], check=True)

        print(f"Updated SSH configuration to use key: {ssh_key_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("Failed to switch Git account.")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to update SSH configuration.")

def add_account(accounts):
    account_name = input("Enter account name: ").strip().lower()
    if account_name in accounts:
        print("Account already exists.")
        return

    name = input("Enter Git user name: ").strip()
    email = input("Enter Git user email: ").strip()
    print("""Do you want to generate SSH key or do you already have one?
1. Already have one 
          """)
    ssh_key = input("Enter path to SSH key: ").strip()

    accounts[account_name] = {
        "name": name,
        "email": email,
        "ssh_key": ssh_key
    }
    save_accounts(accounts)
    print(f"Account '{account_name}' added successfully.")

def remove_account(accounts):
    account_name = input("Enter account name to remove: ").strip().lower()
    if account_name in accounts:
        del accounts[account_name]
        save_accounts(accounts)
        print(f"Account '{account_name}' removed successfully.")
    else:
        print("Account not found.")

def choose_account(accounts):
    print("Available accounts:")
    for account in accounts:
        print(f"- {account}")

    chosen_account = input("Enter the account you want to switch to: ").strip().lower()

    if chosen_account in accounts:
        account_info = accounts[chosen_account]
        switch_git_account(account_info['name'], account_info['email'], account_info['ssh_key'])
    else:
        print("Invalid account. Please try again.")

def main():
    accounts = load_accounts()

    while True:
        print("\nOptions:")
        print("1. Switch account")
        print("2. Add account")
        print("3. Remove account")
        print("4. Quit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            choose_account(accounts)
        elif choice == '2':
            add_account(accounts)
        elif choice == '3':
            remove_account(accounts)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
