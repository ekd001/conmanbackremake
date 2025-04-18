#!/bin/bash

# Affiche l'aide
function show_help() {
    echo "Usage:"
    echo "  $0 projet <nom_du_projet>     # Crée un nouveau projet Django"
    echo "  $0 app <nom_du_projet> <nom_de_l_app>   # Crée une app Django dans un projet existant"
    exit 1
}

# Vérifie qu'au moins 2 arguments sont fournis
if [ "$#" -lt 2 ]; then
    show_help
fi

MODE=$1

# Création d’un projet
if [ "$MODE" = "projet" ]; then
    PROJECT_NAME=$2

    mkdir "$PROJECT_NAME"
    cd "$PROJECT_NAME" || exit

    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv env
    source env/bin/activate

    echo "⬇️ Installation de Django..."
    pip install django

    echo "🚀 Création du projet Django : $PROJECT_NAME"
    django-admin startproject "$PROJECT_NAME" .

    echo "✅ Projet '$PROJECT_NAME' créé avec succès."

# Création d’une app
elif [ "$MODE" = "app" ]; then
    if [ "$#" -ne 3 ]; then
        show_help
    fi

    PROJECT_DIR=$2
    APP_NAME=$3

    cd "$PROJECT_DIR" || exit
    source env/bin/activate

    echo "🧩 Création de l'application Django : $APP_NAME"
    python manage.py startapp "$APP_NAME"

    SETTINGS_FILE="$PROJECT_DIR/settings.py"
    if grep -q "INSTALLED_APPS" "$SETTINGS_FILE"; then
        echo "⚙️ Enregistrement de l'app dans settings.py"
        sed -i "/INSTALLED_APPS = \[/ a\    '$APP_NAME'," "$SETTINGS_FILE"
    else
        echo "⚠️ Impossible de trouver INSTALLED_APPS dans $SETTINGS_FILE"
    fi

    echo "✅ App '$APP_NAME' ajoutée au projet '$PROJECT_DIR'."

else
    show_help
fi
