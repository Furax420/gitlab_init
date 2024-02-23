from tkinter import Tk, Label, Entry, Button, filedialog
import git_operations
from pyad import pyad

def get_ad_user_info():
    """
    Récupère le nom d'utilisateur et l'email depuis Active Directory.
    Nécessite que l'utilisateur ait les droits AD appropriés.
    """
    try:
        # Utilisez votre domaine ici. Exemple : "DC=exemple,DC=com"
        ad_user = pyad.aduser.ADUser.from_cn(pyad.pyad_setdefaults.get_current_user())
        username = ad_user.get_attribute("sAMAccountName")[0]
        email = ad_user.get_attribute("mail")[0]
        return username, email
    except Exception as e:
        print(f"Erreur lors de la récupération des infos AD: {e}")
        return None, None

def submit():
    username = username_entry.get()
    email = email_entry.get()
    project_name = project_name_entry.get()
    repo_path = repo_path_entry.get()
    try:
        git_operations.git_init_and_remote(repo_path, username, email, project_name)
        git_operations.first_commit_and_push(repo_path)
        print("Dépôt configuré avec succès !")
    except Exception as e:
        print(f"Erreur lors de la configuration du dépôt : {e}")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    repo_path_entry.delete(0, "end")
    repo_path_entry.insert(0, folder_selected)

root = Tk()
root.title("Configuration GitLab")

username, email = get_ad_user_info()

username_label = Label(root, text="Nom d'utilisateur AD :")
username_label.pack()
username_entry = Entry(root)
if username:
    username_entry.insert(0, username)  # Pré-rempli avec le nom d'utilisateur AD
username_entry.pack()

email_label = Label(root, text="Email AD :")
email_label.pack()
email_entry = Entry(root)
if email:
    email_entry.insert(0, email)  # Pré-rempli avec l'email AD
email_entry.pack()

project_name_label = Label(root, text="Nom du projet GitLab :")
project_name_label.pack()
project_name_entry = Entry(root)
project_name_entry.pack()

repo_path_label = Label(root, text="Chemin du dépôt :")
repo_path_label.pack()
repo_path_entry = Entry(root)
repo_path_entry.pack()

browse_button = Button(root, text="Parcourir", command=browse_folder)
browse_button.pack()

submit_button = Button(root, text="Soumettre", command=submit)
submit_button.pack()

root.mainloop()
