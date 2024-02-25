import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QStackedWidget, QFileDialog, QGridLayout, QStyle)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from pyad import aduser

# Supposons que git_init_and_remote et execute_git_command soient définis dans git_operations.py
from git_operations import git_init_and_remote, execute_git_command

def get_user_info_from_ad():
    try:
        current_user = aduser.ADUser.from_cn(aduser.ADUser.get_logged_in_user_name())
        username = current_user.get_attribute("sAMAccountName")[0]
        email = current_user.get_attribute("mail")[0] if current_user.get_attribute("mail") else "Non fourni"
    except Exception as e:
        print(f"Erreur lors de la récupération des informations AD: {e}")
        username = "Utilisateur inconnu"
        email = "email@inconnu.com"
    return username, email

def create_logos_layout():
    logos_layout = QHBoxLayout()
    logos_layout.setAlignment(Qt.AlignCenter)
    
    gitlab_logo = QLabel()
    gitlab_pixmap = QPixmap('sources/gitlab-logo.png')  # Ajustez le chemin d'accès selon votre structure de fichiers
    gitlab_logo.setPixmap(gitlab_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
    
    uerx_logo = QLabel()
    uerx_pixmap = QPixmap('sources/uerx-logo.png')  # Ajustez le chemin d'accès selon votre structure de fichiers
    uerx_logo.setPixmap(uerx_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
    

    logos_layout.addWidget(gitlab_logo)
    logos_layout.addWidget(uerx_logo)
    return logos_layout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Configuration GitLab')
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #333; color: white;")

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.user_info_page = UserInfoPage(self)
        self.project_info_page = ProjectInfoPage(self)

        self.central_widget.addWidget(self.user_info_page)
        self.central_widget.addWidget(self.project_info_page)

    def goToProjectInfoPage(self):
        self.central_widget.setCurrentWidget(self.project_info_page)

    def goToUserInfoPage(self):
        self.central_widget.setCurrentWidget(self.user_info_page)


class UserInfoPage(QWidget):
    # ... Autres parties de la classe ...

    def __init__(self, parent):
        super().__init__(parent)
        main_layout = QVBoxLayout()
        content_layout = QVBoxLayout()
        content_layout.addLayout(create_logos_layout())
        title = QLabel("Étape 1: Informations Utilisateur")
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)

        grid_layout = QGridLayout()

        username, email = get_user_info_from_ad()

        # Ajoutez les labels et les champs de texte à la grille
        username_label = QLabel("Nom d'utilisateur:")
        username_line_edit_container = QWidget()
        username_h_layout = QHBoxLayout(username_line_edit_container)
        self.username_line_edit = QLineEdit()
        self.username_line_edit.setMaximumWidth(400)
        self.username_line_edit.setText(username)
        username_h_layout.addWidget(self.username_line_edit)
        username_h_layout.addStretch()
        grid_layout.addWidget(username_label, 0, 0)
        grid_layout.addWidget(username_line_edit_container, 0, 1)

        email_label = QLabel("Email:")
        email_line_edit_container = QWidget()
        email_h_layout = QHBoxLayout(email_line_edit_container)
        self.email_line_edit = QLineEdit()
        self.email_line_edit.setMaximumWidth(400)
        self.email_line_edit.setText(email)
        email_h_layout.addWidget(self.email_line_edit)
        email_h_layout.addStretch()
        grid_layout.addWidget(email_label, 1, 0)
        grid_layout.addWidget(email_line_edit_container, 1, 1)

        # Bouton Suivant
        next_button_layout = QHBoxLayout()
        next_button_layout.addStretch()
        next_button = QPushButton("Suivant")
        next_button.clicked.connect(parent.goToProjectInfoPage)
        next_button_layout.addWidget(next_button)
        next_button_layout.addStretch()
        grid_layout.addLayout(next_button_layout, 2, 0, 1, 2)

        content_layout.addLayout(grid_layout)
        main_layout.addStretch()
        main_layout.addLayout(content_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)


class ProjectInfoPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Conserve une référence à la fenêtre principale

        main_layout = QVBoxLayout()
        content_layout = QVBoxLayout()
        content_layout.addLayout(create_logos_layout())
        title = QLabel("Étape 2: Informations du Projet GitLab")
        title.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title)



        # Configuration du QGridLayout
        grid_layout = QGridLayout()

        # Configuration des champs de saisie et des boutons
        self.repo_path_line_edit = QLineEdit()
        self.repo_path_line_edit.setPlaceholderText("Chemin du dossier de code")
        self.repo_path_line_edit.setMaximumWidth(400)


        browse_button_layout = QHBoxLayout()
        browse_button_layout.addStretch()
        browse_button = QPushButton("Parcourir")
        browse_button_layout.addWidget(browse_button)
        browse_button_layout.addStretch()
        browse_button.clicked.connect(self.browse_folder)
        browse_button.setMaximumWidth(100)

        self.project_name_line_edit = QLineEdit()
        self.project_name_line_edit.setPlaceholderText("Nom du projet GitLab")
        self.project_name_line_edit.setMaximumWidth(400)

        # Ajout des champs de saisie et des boutons au grid_layout
        grid_layout.addWidget(self.repo_path_line_edit, 0, 0)
        grid_layout.addWidget(browse_button, 0, 1)
        grid_layout.addWidget(self.project_name_line_edit, 1, 0)

        # Bouton Valider
        validate_button_layout = QHBoxLayout()
        validate_button_layout.addStretch()
        validate_button = QPushButton("Valider")
        validate_button.clicked.connect(self.on_validate_clicked)
        validate_button_layout.addWidget(validate_button)
        validate_button_layout.addStretch()
        grid_layout.addLayout(validate_button_layout, 2, 0, 1, 2)

        content_layout.addLayout(grid_layout)
        main_layout.addStretch()
        main_layout.addLayout(content_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)



    def goToUserInfoPage(self):
        self.parent.goToUserInfoPage()

    def on_validate_clicked(self):
        repo_path = self.repo_path_line_edit.text()
        project_name = self.project_name_line_edit.text()
        # Ici, vous pouvez appeler la fonction qui exécute les commandes Git avec les paramètres récupérés
        print(f"Exécution des commandes Git pour {project_name} dans {repo_path}")

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Sélectionnez un dossier")
        if folder:
            self.repo_path_line_edit.setText(folder)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()  # Correction pour appeler correctement la fonction main
