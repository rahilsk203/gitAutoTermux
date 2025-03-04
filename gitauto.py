#!/usr/bin/env python3
import os
import json
import subprocess
import requests

# Constants
CREDENTIALS_FILE = os.path.expanduser("~/.git_credentials.json")
GITHUB_API = "https://api.github.com"

# ======= Authentication System =======
def load_credentials():
    """Load saved GitHub credentials."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_credentials(username, token):
    """Save GitHub credentials securely."""
    credentials = {"username": username, "token": token}
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)
    print("✅ GitHub credentials saved!")

def git_login():
    """Login using GitHub username & token."""
    credentials = load_credentials()
    if credentials:
        print(f"✅ Already logged in as {credentials['username']}")
        return credentials

    username = input("Enter GitHub username: ")
    token = input("Enter GitHub Personal Access Token (PAT): ")

    save_credentials(username, token)
    return {"username": username, "token": token}

# ======= Git Operations =======
def execute_command(command):
    """Execute shell commands with error handling."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing command: {e}")

def repo_exists(repo_name):
    """Check if repo or folder already exists."""
    credentials = git_login()
    folder_exists = os.path.exists(repo_name)

    url = f"{GITHUB_API}/repos/{credentials['username']}/{repo_name}"
    headers = {"Authorization": f"token {credentials['token']}"}
    response = requests.get(url, headers=headers)

    remote_exists = response.status_code == 200

    if folder_exists:
        print(f"⚠️ Folder '{repo_name}' already exists!")
    if remote_exists:
        print(f"⚠️ GitHub repository '{repo_name}' already exists!")

    return folder_exists or remote_exists

def create_repo(repo_name, private=True):
    """Create a new GitHub repository."""
    if repo_exists(repo_name):
        print("❌ Repository creation aborted!")
        return

    credentials = git_login()
    url = f"{GITHUB_API}/user/repos"
    headers = {"Authorization": f"token {credentials['token']}"}
    data = {"name": repo_name, "private": private}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"✅ Repository '{repo_name}' created successfully!")
        auto_clone(repo_name)
    else:
        print(f"❌ Error: {response.json()}")

def auto_clone(repo_name):
    """Automatically clone, enter the repo, and exit script."""
    credentials = git_login()
    repo_url = f"https://{credentials['username']}:{credentials['token']}@github.com/{credentials['username']}/{repo_name}.git"

    print(f"📥 Cloning {repo_name}...")
    execute_command(["git", "clone", repo_url])

    if os.path.exists(repo_name):
        os.chdir(repo_name)  # Enter the cloned repo folder
        print(f"📂 Entered into '{repo_name}'")
        print("👋 Exiting script...")
        exit()
    else:
        print("❌ Clone failed!")

def delete_repo(repo_name):
    """Delete repository from GitHub & local system."""
    credentials = git_login()
    url = f"{GITHUB_API}/repos/{credentials['username']}/{repo_name}"
    headers = {"Authorization": f"token {credentials['token']}"}

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"✅ Repository '{repo_name}' deleted successfully!")
        if os.path.exists(repo_name):
            execute_command(["rm", "-rf", repo_name])
            print(f"🗑️ Local folder '{repo_name}' deleted!")
    else:
        print(f"❌ Error: {response.json()}")

def set_repo_visibility(repo_name, private):
    """Set repository visibility (private/public)."""
    credentials = git_login()
    url = f"{GITHUB_API}/repos/{credentials['username']}/{repo_name}"
    headers = {"Authorization": f"token {credentials['token']}"}
    data = {"private": private}

    response = requests.patch(url, json=data, headers=headers)

    if response.status_code == 200:
        status = "Private" if private else "Public"
        print(f"✅ Repository '{repo_name}' is now {status}!")
    else:
        print(f"❌ Error: {response.json()}")

def push_repo():
    """Push latest changes to GitHub with stored authentication."""
    if not os.path.exists(".git"):
        print("❌ This is not a Git repository!")
        return

    credentials = load_credentials()
    if not credentials:
        print("❌ No GitHub credentials found! Please login first.")
        return

    execute_command(["git", "add", "."])
    commit_message = input("Enter commit message: ").strip()
    if not commit_message:
        commit_message = "Auto commit"
    execute_command(["git", "commit", "-m", commit_message])
    execute_command(["git", "push"])

def clone_public_repo():
    """Clone any public GitHub repository and enter the folder."""
    repo_url = input("Enter public Git repository URL: ").strip()
    
    if not repo_url:
        print("❌ Invalid URL!")
        return

    print(f"📥 Cloning {repo_url}...")
    execute_command(["git", "clone", repo_url])

    repo_name = repo_url.split("/")[-1].replace(".git", "")  # Extract repo name

    if os.path.exists(repo_name):
        os.chdir(repo_name)  # Enter the cloned repo folder
        print(f"📂 Entered into '{repo_name}'")
        print("👋 Exiting script...")
        exit()
    else:
        print("❌ Clone failed!")

# ======= New Features =======
def pull_repo():
    """Pull latest changes from GitHub."""
    if not os.path.exists(".git"):
        print("❌ This is not a Git repository!")
        return

    execute_command(["git", "pull"])

def create_branch(branch_name):
    """Create and switch to a new branch."""
    execute_command(["git", "checkout", "-b", branch_name])

def list_branches():
    """List all branches."""
    execute_command(["git", "branch"])

def switch_branch(branch_name):
    """Switch to an existing branch."""
    execute_command(["git", "checkout", branch_name])

def show_status():
    """Show the current repository status."""
    execute_command(["git", "status"])

def show_commit_history():
    """Show the commit history."""
    execute_command(["git", "log", "--oneline"])

# ======= Main Menu =======
def main():
    """User command menu."""
    inside_git_repo = os.path.exists(".git")

    while True:
        print("\n📌 Choose an option:")
        
        if not inside_git_repo:
            print(" 1️⃣  Create Repository")
            print(" 5️⃣  Clone Public Repository")
        else:
            print(" 4️⃣  Push to Repository")
            print(" 7️⃣  Pull Latest Changes")
            print(" 8️⃣  Branch Management")
            print(" 9️⃣  Show Status")
            print(" 0️⃣  Show Commit History")
        
        print(" 2️⃣  Delete Repository")
        print(" 3️⃣  Make Repository Private/Public")
        print(" 6️⃣  Exit")

        choice = input("Enter choice: ")

        if choice == "1" and not inside_git_repo:
            repo_name = input("Enter repository name: ")
            private = input("Private repo? (yes/no): ").strip().lower() == "yes"
            create_repo(repo_name, private)

        elif choice == "2":
            repo_name = input("Enter repository name to delete: ")
            delete_repo(repo_name)

        elif choice == "3":
            repo_name = input("Enter repository name: ")
            private = input("Make Private? (yes/no): ").strip().lower() == "yes"
            set_repo_visibility(repo_name, private)

        elif choice == "4" and inside_git_repo:
            push_repo()

        elif choice == "5" and not inside_git_repo:
            clone_public_repo()

        elif choice == "6":
            print("👋 Exiting...!")
            break

        elif choice == "7" and inside_git_repo:
            pull_repo()

        elif choice == "8" and inside_git_repo:
            print("\n📌 Branch Management:")
            print(" a) Create new branch")
            print(" b) List branches")
            print(" c) Switch branch")
            sub_choice = input("Enter choice (a/b/c): ").strip().lower()
            if sub_choice == "a":
                branch_name = input("Enter new branch name: ")
                create_branch(branch_name)
            elif sub_choice == "b":
                list_branches()
            elif sub_choice == "c":
                branch_name = input("Enter branch name to switch to: ")
                switch_branch(branch_name)
            else:
                print("❌ Invalid option!")

        elif choice == "9" and inside_git_repo:
            show_status()

        elif choice == "0" and inside_git_repo:
            show_commit_history()

        else:
            print("❌ Invalid or hidden option!")

        # Update inside_git_repo status after each action
        inside_git_repo = os.path.exists(".git")

if __name__ == "__main__":
    main()
