# API REST de gestion d'étudiants & Pipeline CI/CD

Projet réalisé dans le cadre du TP - Chapitre 1 (CI/CD). Il s'agit d'une API REST développée en **Python (Flask)**, testée avec **pytest**, vérifiée par le linter **flake8** et intégrée via un pipeline **GitHub Actions**.

## Fonctionnalités de l'API

L'API gère un annuaire d'étudiants stocké en mémoire avec 7 endpoints :
- `GET /students` : Liste tous les étudiants
- `GET /students/:id` : Récupère un étudiant par son ID
- `POST /students` : Crée un nouvel étudiant (validations strictes)
- `PUT /students/:id` : Modifie un étudiant existant
- `DELETE /students/:id` : Supprime un étudiant
- `GET /students/stats` : Retourne des statistiques (moyenne, effectif par filière, meilleur étudiant)
- `GET /students/search?q=...` : Recherche par nom ou prénom

## Installation & Lancement local

1. **Cloner le projet :**
    ```bash
    git clone https://github.com/lycapi/tp-cicd.git
    cd tp-cicd
    ```

2. **Créer et activer l'environnement virtuel :**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Installer les dépendances :**
    ```bash
    pip install -r requirements.txt
    ```

4. **Lancer l'application :**
    ```bash
    python main.py
    ```

## Qualité du code & Tests

- **Exécuter le linter (analyse statique) :**
  ```bash
  flake8 .