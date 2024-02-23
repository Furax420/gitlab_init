import subprocess
import os

def execute_git_command(command, cwd=None):
    """
    Exécute une commande git dans le répertoire spécifié.
    """
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Erreur lors de l'exécution de la commande git: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')

def git_init_and_remote(repo_path, username, email, project_name):
    """
    Initialise un dépôt Git, configure l'utilisateur et ajoute un remote.
    """
    # Configure Git user si non configuré
    try:
        execute_git_command(f"git config user.name \"{username}\"", cwd=repo_path)
        execute_git_command(f"git config user.email \"{email}\"", cwd=repo_path)
    except Exception as e:
        print(f"Erreur de configuration Git: {e}")

    # Initialise le dépôt Git si .git n'existe pas
    if not os.path.exists(os.path.join(repo_path, ".git")):
        execute_git_command("git init", cwd=repo_path)

    # Ajoute un fichier .gitignore
    with open(os.path.join(repo_path, ".gitignore"), 'w') as gitignore:
        gitignore.write(".DS_Store\n")
    
    # Ajoute le remote
    remote_url = f"http://gitlab.local/{username}/{project_name}.git"
    execute_git_command(f"git remote add origin {remote_url}", cwd=repo_path)

def first_commit_and_push(repo_path):
    """
    Effectue le premier commit et push sur le dépôt.
    """
    execute_git_command("git add .", cwd=repo_path)
    execute_git_command('git commit -m "Initial commit from script"', cwd=repo_path)
    execute_git_command("git push -u origin master", cwd=repo_path)


# Path: ui.py